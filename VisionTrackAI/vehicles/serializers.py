from rest_framework import serializers
from .models import Vehicle, VehicleDetection


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class VehicleDetectionSerializer(serializers.ModelSerializer):
    plate_number = serializers.CharField(source='vehicle.plate_number', read_only=True)

    class Meta:
        model = VehicleDetection
        fields = '__all__'
