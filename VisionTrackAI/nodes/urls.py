from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'nodes'

router = DefaultRouter()
router.register(r'nodes', views.EdgeNodeViewSet)
router.register(r'logs', views.NodeLogViewSet)

urlpatterns = [
    path('', views.node_list, name='node_list'),
    path('<int:pk>/', views.node_detail, name='node_detail'),
    path('<int:pk>/config/', views.node_config, name='node_config'),
    path('<int:pk>/export/', views.node_logs_export, name='node_logs_export'),
    path('api/', include(router.urls)),
]
