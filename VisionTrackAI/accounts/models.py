from django.db import models
from django.contrib.auth.models import User
import random


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
        ('analyst', 'Analyst'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    organization = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class OTPVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        return self.otp

    def __str__(self):
        return f"OTP for {self.user.username}"


class AccessRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='access_requests')
    requested_role = models.CharField(max_length=20)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reason = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.requested_role} ({self.status})"


class UserDocument(models.Model):
    DOC_TYPE_CHOICES = [
        ('id_proof', 'ID Proof'),
        ('org_letter', 'Organization Letter'),
        ('certification', 'Certification'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default='other')
    file = models.FileField(upload_to='documents/')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
