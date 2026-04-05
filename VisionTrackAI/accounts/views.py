from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from .models import UserProfile, OTPVerification, AccessRequest, UserDocument
from .serializers import AccessRequestSerializer, UserDocumentSerializer


def admin_required(view_func):
    """Decorator that restricts access to superusers/admins only."""
    decorated = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url='/accounts/login/'
    )(view_func)
    return login_required(decorated)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone', '')
        organization = request.POST.get('organization', '')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        UserProfile.objects.create(user=user, phone=phone, organization=organization)

        # Generate OTP
        otp = OTPVerification.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(minutes=10)
        )
        otp.generate_otp()
        otp.save()

        login(request, user)
        return redirect('accounts:otp_verify')

    return render(request, 'accounts/signup.html')


@login_required
def otp_verify_view(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        try:
            otp_obj = OTPVerification.objects.filter(
                user=request.user, is_verified=False
            ).latest('created_at')
            if otp_obj.otp == entered_otp and otp_obj.expires_at > timezone.now():
                otp_obj.is_verified = True
                otp_obj.save()
                profile = request.user.profile
                profile.is_verified = True
                profile.save()
                return redirect('accounts:verify_success')
            else:
                messages.error(request, 'Invalid or expired OTP.')
        except OTPVerification.DoesNotExist:
            messages.error(request, 'No OTP found. Please request a new one.')
    # Show OTP for dev/demo purposes
    otp_obj = OTPVerification.objects.filter(user=request.user, is_verified=False).last()
    return render(request, 'accounts/otp_verify.html', {'otp_hint': otp_obj.otp if otp_obj else ''})


@login_required
def verify_success_view(request):
    return render(request, 'accounts/verify_success.html')


@login_required
def onboarding_view(request):
    step = int(request.GET.get('step', 1))
    if request.method == 'POST':
        if step >= 4:
            profile = request.user.profile
            profile.onboarding_completed = True
            profile.save()
            return redirect('dashboard:home')
        return redirect(f'/accounts/onboarding/?step={step + 1}')
    return render(request, 'accounts/onboarding.html', {'step': step})


def logout_view(request):
    logout(request)
    return redirect('accounts:login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        # Update Profile fields
        profile.phone = request.POST.get('phone', '')
        profile.organization = request.POST.get('organization', '')
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:profile')
    docs_count = request.user.documents.count()
    access_requests = request.user.access_requests.all()[:5]
    context = {
        'profile': profile,
        'docs_count': docs_count,
        'access_requests': access_requests,
    }
    return render(request, 'accounts/profile.html', context)


@admin_required
def access_management_view(request):
    pending_requests = AccessRequest.objects.filter(status='pending').order_by('-created_at')
    approved_requests = AccessRequest.objects.filter(status='approved').order_by('-reviewed_at')[:5]
    rejected_requests = AccessRequest.objects.filter(status='rejected').order_by('-reviewed_at')[:5]
    users = User.objects.select_related('profile').all().order_by('-date_joined')

    # Role counts
    role_counts = {
        'admin': UserProfile.objects.filter(role='admin').count(),
        'operator': UserProfile.objects.filter(role='operator').count(),
        'viewer': UserProfile.objects.filter(role='viewer').count(),
        'analyst': UserProfile.objects.filter(role='analyst').count(),
    }
    total_users = User.objects.count()
    verified_users = UserProfile.objects.filter(is_verified=True).count()

    # Search filter
    search = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    if search:
        users = users.filter(
            models.Q(username__icontains=search) |
            models.Q(email__icontains=search) |
            models.Q(first_name__icontains=search) |
            models.Q(last_name__icontains=search)
        )
    if role_filter:
        users = users.filter(profile__role=role_filter)

    context = {
        'pending_requests': pending_requests,
        'approved_requests': approved_requests,
        'rejected_requests': rejected_requests,
        'users': users,
        'role_counts': role_counts,
        'total_users': total_users,
        'verified_users': verified_users,
        'search': search,
        'role_filter': role_filter,
    }
    return render(request, 'accounts/access_management.html', context)


@login_required
def access_request_view(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        reason = request.POST.get('reason', '')
        AccessRequest.objects.create(user=request.user, requested_role=role, reason=reason)
        messages.success(request, 'Access request submitted.')
        return redirect('accounts:access_management')
    return render(request, 'accounts/access_request.html')


@admin_required
def access_review_view(request, pk):
    access_req = get_object_or_404(AccessRequest, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        access_req.status = action
        access_req.reviewed_by = request.user
        access_req.reviewed_at = timezone.now()
        access_req.save()
        if action == 'approved':
            profile = access_req.user.profile
            profile.role = access_req.requested_role
            profile.save()
    return redirect('accounts:access_management')


@login_required
def documents_view(request):
    docs = UserDocument.objects.filter(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        doc_type = request.POST.get('doc_type', 'other')
        file = request.FILES.get('file')
        if file:
            UserDocument.objects.create(user=request.user, title=title, doc_type=doc_type, file=file)
            messages.success(request, 'Document uploaded.')
        return redirect('accounts:documents')
    return render(request, 'accounts/documents.html', {'documents': docs})


@login_required
def document_delete_view(request, pk):
    doc = get_object_or_404(UserDocument, pk=pk, user=request.user)
    doc.delete()
    messages.success(request, 'Document deleted.')
    return redirect('accounts:documents')


# API Views
class AccessRequestViewSet(viewsets.ModelViewSet):
    queryset = AccessRequest.objects.all()
    serializer_class = AccessRequestSerializer


class UserDocumentViewSet(viewsets.ModelViewSet):
    serializer_class = UserDocumentSerializer

    def get_queryset(self):
        return UserDocument.objects.filter(user=self.request.user)
