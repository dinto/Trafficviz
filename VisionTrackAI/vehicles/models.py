from django.db import models


class Vehicle(models.Model):
    plate_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=30, blank=True)
    make = models.CharField(max_length=50, blank=True)
    model = models.CharField(max_length=50, blank=True)
    owner = models.CharField(max_length=100, blank=True)
    is_flagged = models.BooleanField(default=False)
    flag_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plate_number


class VehicleDetection(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='detections')
    node_name = models.CharField(max_length=100)
    confidence = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    speed = models.FloatField(default=0, blank=True)
    snapshot = models.ImageField(upload_to='detections/', blank=True, null=True)
    detected_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-detected_at']

    def __str__(self):
        return f"{self.vehicle.plate_number} at {self.node_name}"


class TrackingPoint(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='tracking_points')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField()

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.vehicle.plate_number} @ ({self.latitude}, {self.longitude})"
