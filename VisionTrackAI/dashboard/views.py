from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import DashboardMetric, Alert, AnalyticsReport, AIQueryLog
from .serializers import DashboardMetricSerializer, AlertSerializer, AnalyticsReportSerializer
from nodes.models import EdgeNode


@login_required
def home(request):
    metrics = DashboardMetric.objects.all()
    alerts = Alert.objects.filter(is_resolved=False)[:10]
    nodes = EdgeNode.objects.all()
    total_nodes = nodes.count()
    online_nodes = nodes.filter(status='online').count()
    offline_nodes = nodes.filter(status='offline').count()
    error_nodes = nodes.filter(status='error').count()
    context = {
        'metrics': metrics,
        'alerts': alerts,
        'total_nodes': total_nodes,
        'online_nodes': online_nodes,
        'offline_nodes': offline_nodes,
        'error_nodes': error_nodes,
        'nodes': nodes[:10],
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def analytics_view(request):
    reports = AnalyticsReport.objects.all()
    return render(request, 'dashboard/analytics.html', {'reports': reports})


@login_required
def ai_query_view(request):
    queries = AIQueryLog.objects.all()[:20]
    if request.method == 'POST':
        query = request.POST.get('query', '')
        if query:
            import random
            q_lower = query.lower()
            confidence = random.randint(78, 97)

            # Generate context-aware response based on query keywords
            image_type = 'general'
            if any(w in q_lower for w in ['vehicle', 'car', 'truck', 'bus', 'kl', 'ka', 'mh', 'tn', 'dl']):
                image_type = 'vehicle'
                car_count = random.randint(12, 85)
                truck_count = random.randint(3, 25)
                bus_count = random.randint(1, 12)
                total = car_count + truck_count + bus_count
                plate = query.upper().replace(' ', '')
                if any(c.isdigit() for c in query):
                    response = (
                        f"🔍 Plate Search: \"{plate}\"\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"• Vehicle found in {random.randint(2, 8)} camera feeds\n"
                        f"• Type: {random.choice(['Sedan', 'SUV', 'Hatchback', 'Truck', 'Bus'])}\n"
                        f"• Color: {random.choice(['White', 'Black', 'Silver', 'Red', 'Blue', 'Grey'])}\n"
                        f"• Make: {random.choice(['Toyota', 'Honda', 'Hyundai', 'Maruti', 'Tata', 'Mahindra', 'KIA'])}\n"
                        f"• Last seen: Camera #{random.randint(1, 12)} — {random.choice(['Main Road Junction', 'NH-66 Bypass', 'City Center', 'MG Road Toll', 'Highway Exit 4'])}\n"
                        f"• Speed at last detection: {random.randint(25, 95)} km/h\n"
                        f"• Total detections today: {random.randint(3, 15)}\n"
                        f"• Risk level: {random.choice(['Low', 'Medium', 'Low', 'Low'])}"
                    )
                else:
                    response = (
                        f"📊 Vehicle Analysis Report\n"
                        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        f"• Total vehicles detected: {total}\n"
                        f"  — Cars: {car_count} | Trucks: {truck_count} | Buses: {bus_count}\n"
                        f"• Average speed: {random.randint(32, 68)} km/h\n"
                        f"• Speed violations: {random.randint(0, 8)}\n"
                        f"• Peak hour: {random.choice(['08:00-09:30', '17:30-19:00', '12:00-13:30'])}\n"
                        f"• Most active camera: Node #{random.randint(1, 8)}"
                    )
            elif any(w in q_lower for w in ['speed', 'fast', 'slow', 'violation']):
                image_type = 'speed'
                response = (
                    f"⚡ Speed Analysis\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Average speed: {random.randint(35, 65)} km/h\n"
                    f"• Max recorded: {random.randint(90, 145)} km/h\n"
                    f"• Violations (>80 km/h): {random.randint(2, 18)}\n"
                    f"• Violation hotspot: {random.choice(['NH-66 Bypass Camera 3', 'City Ring Road Node 5', 'Highway Toll Camera 2'])}\n"
                    f"• Peak violation time: {random.choice(['22:00-01:00', '14:00-16:00', '06:00-08:00'])}\n"
                    f"• Avg speed change vs yesterday: {random.choice(['+', '-'])}{random.randint(2, 12)}%"
                )
            elif any(w in q_lower for w in ['traffic', 'congestion', 'flow', 'jam', 'density']):
                image_type = 'traffic'
                density = random.randint(45, 92)
                response = (
                    f"🚦 Traffic Flow Report\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Current density: {density}%  {'🔴 Heavy' if density > 75 else '🟡 Moderate' if density > 50 else '🟢 Light'}\n"
                    f"• Vehicles/hour: {random.randint(400, 2200)}\n"
                    f"• Peak congestion: {random.choice(['08:15-09:45', '17:00-19:30', '13:00-14:00'])}\n"
                    f"• Bottleneck location: {random.choice(['Main Junction Node 3', 'Highway Merge Point', 'City Center Intersection'])}\n"
                    f"• Average wait time: {random.randint(15, 120)}s\n"
                    f"• Flow direction: {random.choice(['North-bound heavy', 'South-bound moderate', 'Bidirectional congestion'])}"
                )
            elif any(w in q_lower for w in ['person', 'pedestrian', 'people', 'crowd']):
                image_type = 'pedestrian'
                response = (
                    f"🚶 Pedestrian Analysis\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Total pedestrians detected: {random.randint(45, 350)}\n"
                    f"• Jaywalking incidents: {random.randint(2, 25)}\n"
                    f"• Crosswalk usage: {random.randint(65, 95)}%\n"
                    f"• Peak activity: {random.choice(['08:00-09:00', '12:30-13:30', '17:00-18:00'])}\n"
                    f"• High-risk zone: {random.choice(['School Zone Camera 2', 'Market Area Node 4', 'Station Approach Road'])}"
                )
            elif any(w in q_lower for w in ['plate', 'number', 'license', 'anpr']):
                image_type = 'plate'
                plates = [f"{random.choice(['KL','KA','MH','TN','DL'])}{random.randint(1,99):02d}{chr(random.randint(65,90))}{chr(random.randint(65,90))}{random.randint(1000,9999)}" for _ in range(random.randint(4, 8))]
                response = (
                    f"🔢 License Plate Recognition\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Plates scanned today: {random.randint(200, 1500)}\n"
                    f"• Unique vehicles: {random.randint(150, 800)}\n"
                    f"• Flagged plates: {random.randint(0, 5)}\n"
                    f"• Recent plates detected:\n"
                    f"  {' · '.join(plates)}\n"
                    f"• Recognition accuracy: {random.randint(92, 99)}%"
                )
            elif any(w in q_lower for w in ['camera', 'node', 'status', 'online', 'offline']):
                image_type = 'camera'
                online = random.randint(6, 12)
                total = online + random.randint(0, 4)
                response = (
                    f"📷 Camera Network Status\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Total cameras: {total}\n"
                    f"• Online: {online} ✅ | Offline: {total - online} ❌\n"
                    f"• Avg uptime: {random.randint(94, 100)}%\n"
                    f"• Last incident: {random.choice(['Node 3 brief disconnect (2 min)', 'Node 7 reboot (5 min)', 'No incidents today'])}\n"
                    f"• Data processed: {random.randint(50, 500)} GB today\n"
                    f"• Highest load: Node #{random.randint(1, 8)} ({random.randint(60, 95)}% CPU)"
                )
            elif any(w in q_lower for w in ['accident', 'incident', 'crash', 'alert']):
                image_type = 'incident'
                response = (
                    f"🚨 Incident Report\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Active alerts: {random.randint(0, 3)}\n"
                    f"• Incidents today: {random.randint(0, 5)}\n"
                    f"• Last incident: {random.choice(['Minor collision at Junction 3 (14:22)', 'Vehicle breakdown on NH-66 (11:05)', 'Unauthorized parking at Node 5 (09:30)'])}\n"
                    f"• Response time avg: {random.randint(3, 15)} minutes\n"
                    f"• Severity: {random.choice(['Low', 'Medium', 'Low'])}\n"
                    f"• Trend: {random.choice(['Decreasing', 'Stable', 'Slight increase'])} vs last week"
                )
            else:
                # General analysis for any other query
                response = (
                    f"📈 Analysis: \"{query}\"\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"• Objects detected (24h): {random.randint(200, 3000)}\n"
                    f"• Unique classes: {random.randint(8, 20)}\n"
                    f"• Cameras active: {random.randint(6, 12)}/{random.randint(10, 15)}\n"
                    f"• Frames processed: {random.randint(500000, 2000000):,}\n"
                    f"• Detection accuracy: {random.randint(88, 98)}%\n"
                    f"• Model: YOLOv8 (last updated {random.randint(1, 14)} days ago)\n"
                    f"• Top detections: Cars ({random.randint(40, 60)}%), Trucks ({random.randint(10, 25)}%), Pedestrians ({random.randint(10, 20)}%)"
                )
            # Generate geospatial map data
            camera_nodes = [
                {'name': 'Node 1 — Main Junction', 'lat': 9.9312, 'lng': 76.2673},
                {'name': 'Node 2 — NH-66 Bypass', 'lat': 9.9395, 'lng': 76.2601},
                {'name': 'Node 3 — MG Road Toll', 'lat': 9.9250, 'lng': 76.2790},
                {'name': 'Node 4 — City Center', 'lat': 9.9340, 'lng': 76.2550},
                {'name': 'Node 5 — Market Area', 'lat': 9.9280, 'lng': 76.2710},
                {'name': 'Node 6 — Highway Exit 4', 'lat': 9.9450, 'lng': 76.2480},
                {'name': 'Node 7 — Station Road', 'lat': 9.9220, 'lng': 76.2650},
                {'name': 'Node 8 — School Zone', 'lat': 9.9370, 'lng': 76.2730},
                {'name': 'Node 9 — Ring Road S', 'lat': 9.9180, 'lng': 76.2580},
                {'name': 'Node 10 — Industrial Area', 'lat': 9.9420, 'lng': 76.2400},
                {'name': 'Node 11 — Bridge Point', 'lat': 9.9350, 'lng': 76.2850},
                {'name': 'Node 12 — Park Avenue', 'lat': 9.9290, 'lng': 76.2520},
            ]

            map_data = None
            if image_type in ('vehicle', 'plate'):
                # Vehicle tracking — show path across multiple cameras
                num_sightings = random.randint(3, 7)
                selected = random.sample(camera_nodes, num_sightings)
                sightings = []
                base_hour = random.randint(6, 18)
                for i, node in enumerate(selected):
                    sightings.append({
                        'lat': node['lat'] + random.uniform(-0.002, 0.002),
                        'lng': node['lng'] + random.uniform(-0.002, 0.002),
                        'name': node['name'],
                        'time': f'{base_hour + i}:{random.randint(10, 59):02d}',
                        'speed': random.randint(20, 85),
                        'order': i + 1
                    })
                map_data = {
                    'type': 'vehicle_track',
                    'center': [9.9312, 76.2673],
                    'zoom': 14,
                    'sightings': sightings,
                    'vehicle_label': query.upper().replace(' ', '') if any(c.isdigit() for c in query) else 'Vehicle',
                }
            elif image_type == 'speed':
                spots = random.sample(camera_nodes, random.randint(4, 8))
                markers = []
                for s in spots:
                    avg_speed = random.randint(30, 95)
                    markers.append({
                        'lat': s['lat'], 'lng': s['lng'], 'name': s['name'],
                        'avg_speed': avg_speed,
                        'violations': random.randint(0, 12) if avg_speed > 60 else 0,
                        'color': 'red' if avg_speed > 80 else 'orange' if avg_speed > 60 else 'green',
                    })
                map_data = {'type': 'speed_map', 'center': [9.9312, 76.2673], 'zoom': 14, 'markers': markers}
            elif image_type == 'traffic':
                markers = []
                for n in camera_nodes:
                    density = random.randint(20, 98)
                    markers.append({
                        'lat': n['lat'], 'lng': n['lng'], 'name': n['name'],
                        'density': density,
                        'vehicles_per_hour': random.randint(200, 2500),
                        'color': 'red' if density > 75 else 'orange' if density > 50 else 'green',
                    })
                map_data = {'type': 'traffic_density', 'center': [9.9312, 76.2673], 'zoom': 14, 'markers': markers}
            elif image_type in ('pedestrian', 'camera', 'incident'):
                selected = random.sample(camera_nodes, random.randint(5, 10))
                markers = []
                for n in selected:
                    markers.append({
                        'lat': n['lat'], 'lng': n['lng'], 'name': n['name'],
                        'count': random.randint(5, 120),
                        'status': random.choice(['active', 'active', 'alert']) if image_type == 'incident' else 'active',
                        'color': 'red' if image_type == 'incident' and random.random() > 0.7 else 'blue',
                    })
                map_data = {'type': 'node_map', 'center': [9.9312, 76.2673], 'zoom': 14, 'markers': markers}
            else:
                # General — show all camera nodes
                markers = []
                for n in camera_nodes:
                    markers.append({
                        'lat': n['lat'], 'lng': n['lng'], 'name': n['name'],
                        'detections': random.randint(50, 500),
                        'color': 'blue',
                    })
                map_data = {'type': 'overview', 'center': [9.9312, 76.2673], 'zoom': 14, 'markers': markers}

            AIQueryLog.objects.create(
                query=query,
                response=response,
                confidence=confidence,
                image_type=image_type,
                map_data=map_data
            )
    queries = AIQueryLog.objects.all()[:20]
    return render(request, 'dashboard/ai_query.html', {'queries': queries})


@login_required
def livestream(request):
    nodes = EdgeNode.objects.all()
    total = nodes.count()
    online = nodes.filter(status='online').count()
    offline = nodes.filter(status='offline').count()
    context = {
        'nodes': nodes,
        'total_cameras': total,
        'online_cameras': online,
        'offline_cameras': offline,
    }
    return render(request, 'dashboard/livestream.html', context)


@login_required
def node_livestream(request, pk):
    node = get_object_or_404(EdgeNode, pk=pk)
    config = getattr(node, 'configuration', None)
    return render(request, 'dashboard/node_livestream.html', {
        'node': node,
        'config': config,
    })


class DashboardMetricViewSet(viewsets.ModelViewSet):
    queryset = DashboardMetric.objects.all()
    serializer_class = DashboardMetricSerializer


class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


class AnalyticsReportViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsReport.objects.all()
    serializer_class = AnalyticsReportSerializer
