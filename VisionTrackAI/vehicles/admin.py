from django.contrib import admin
from .models import Vehicle, VehicleDetection, TrackingPoint

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('plate_number', 'vehicle_type', 'color', 'make', 'model', 'is_flagged')

@admin.register(VehicleDetection)
class VehicleDetectionAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'node_name', 'confidence', 'detected_at')

@admin.register(TrackingPoint)
class TrackingPointAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'latitude', 'longitude', 'timestamp')
