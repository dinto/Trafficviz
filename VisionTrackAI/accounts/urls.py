from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register(r'access-requests', views.AccessRequestViewSet)
router.register(r'documents', views.UserDocumentViewSet, basename='document')

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('otp/', views.otp_verify_view, name='otp_verify'),
    path('verify-success/', views.verify_success_view, name='verify_success'),
    path('onboarding/', views.onboarding_view, name='onboarding'),
    path('logout/', views.logout_view, name='logout'),
    path('access/', views.access_management_view, name='access_management'),
    path('profile/', views.profile_view, name='profile'),
    path('access/request/', views.access_request_view, name='access_request'),
    path('access/<int:pk>/review/', views.access_review_view, name='access_review'),
    path('documents/', views.documents_view, name='documents'),
    path('documents/<int:pk>/delete/', views.document_delete_view, name='document_delete'),
    path('api/', include(router.urls)),
]
