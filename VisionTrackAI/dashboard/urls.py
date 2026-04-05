from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'dashboard'

router = DefaultRouter()
router.register(r'metrics', views.DashboardMetricViewSet)
router.register(r'alerts', views.AlertViewSet)
router.register(r'reports', views.AnalyticsReportViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('ai-query/', views.ai_query_view, name='ai_query'),
    path('livestream/', views.livestream, name='livestream'),
    path('livestream/<int:pk>/', views.node_livestream, name='node_livestream'),
    path('api/', include(router.urls)),
]
