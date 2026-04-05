from django.contrib import admin
from .models import UserProfile, OTPVerification, AccessRequest, UserDocument

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone', 'organization', 'is_verified')

@admin.register(OTPVerification)
class OTPVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'otp', 'is_verified', 'created_at')

@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'requested_role', 'status', 'created_at')

@admin.register(UserDocument)
class UserDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'doc_type', 'status', 'uploaded_at')
