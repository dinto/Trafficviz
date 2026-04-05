from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'vehicles'

router = DefaultRouter()
router.register(r'vehicles', views.VehicleViewSet)
router.register(r'detections', views.VehicleDetectionViewSet)

urlpatterns = [
    path('', views.vehicle_search, name='vehicle_search'),
    path('map/', views.vehicle_map, name='vehicle_map'),
    path('api/', include(router.urls)),
]
