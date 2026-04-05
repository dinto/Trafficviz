from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .models import Vehicle, VehicleDetection, TrackingPoint
from .serializers import VehicleSerializer, VehicleDetectionSerializer


@login_required
def vehicle_search(request):
    vehicles = Vehicle.objects.all()
    search = request.GET.get('search', '')
    vtype = request.GET.get('type', '')
    flagged = request.GET.get('flagged', '')
    if search:
        vehicles = vehicles.filter(plate_number__icontains=search)
    if vtype:
        vehicles = vehicles.filter(vehicle_type=vtype)
    if flagged == 'true':
        vehicles = vehicles.filter(is_flagged=True)
    return render(request, 'vehicles/vehicle_search.html', {'vehicles': vehicles, 'search': search})


@login_required
def vehicle_map(request):
    detections = VehicleDetection.objects.select_related('vehicle').all()[:100]
    points = []
    for d in detections:
        points.append({
            'plate': d.vehicle.plate_number,
            'lat': d.latitude,
            'lng': d.longitude,
            'node': d.node_name,
            'time': d.detected_at.strftime('%Y-%m-%d %H:%M'),
            'flagged': d.vehicle.is_flagged,
        })
    return render(request, 'vehicles/vehicle_map.html', {'points': points, 'detections': detections})


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


class VehicleDetectionViewSet(viewsets.ModelViewSet):
    queryset = VehicleDetection.objects.all()
    serializer_class = VehicleDetectionSerializer
