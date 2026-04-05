from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
import random
from accounts.models import UserProfile
from dashboard.models import DashboardMetric, Alert, AnalyticsReport
from nodes.models import EdgeNode, NodeConfiguration, NodeLog
from vehicles.models import Vehicle, VehicleDetection
from ai_training.models import TrainingJob, TrainingLog, Hyperparameter


class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@visiontrack.ai', 'admin123')
            UserProfile.objects.create(user=admin, role='admin', organization='VisionTrack HQ', is_verified=True, onboarding_completed=True)
            self.stdout.write(self.style.SUCCESS('Created admin user (admin/admin123)'))

        # Dashboard Metrics
        metrics_data = [
            {'name': 'Active Cameras', 'value': '127', 'unit': '', 'icon': 'camera-video-fill', 'change_percent': 5.2, 'is_positive': True, 'order': 1},
            {'name': 'Detections Today', 'value': '3,847', 'unit': '', 'icon': 'eye-fill', 'change_percent': 12.8, 'is_positive': True, 'order': 2},
            {'name': 'Avg Response', 'value': '23', 'unit': 'ms', 'icon': 'speedometer2', 'change_percent': -3.1, 'is_positive': True, 'order': 3},
            {'name': 'System Load', 'value': '68', 'unit': '%', 'icon': 'cpu-fill', 'change_percent': 2.4, 'is_positive': False, 'order': 4},
        ]
        for m in metrics_data:
            DashboardMetric.objects.update_or_create(name=m['name'], defaults=m)

        # Alerts
        alerts_data = [
            {'title': 'Node EN-007 CPU Critical', 'message': 'CPU usage exceeded 95% for 10 minutes. Auto-scaling triggered.', 'severity': 'critical', 'source': 'EN-007'},
            {'title': 'Storage Warning on EN-003', 'message': 'Disk usage at 82%. Consider cleanup or expansion.', 'severity': 'warning', 'source': 'EN-003'},
            {'title': 'New firmware available', 'message': 'Firmware v2.4.1 is available for 12 nodes.', 'severity': 'info', 'source': 'System'},
            {'title': 'Node EN-012 Offline', 'message': 'Node has been unreachable for 5 minutes. Last ping failed.', 'severity': 'critical', 'source': 'EN-012'},
            {'title': 'Model Training Complete', 'message': 'YOLOv8 training job completed with 94.2% accuracy.', 'severity': 'info', 'source': 'AI Studio'},
        ]
        Alert.objects.all().delete()
        for a in alerts_data:
            Alert.objects.create(**a)

        # Analytics Reports
        reports_data = [
            {'title': 'Weekly Node Health Report', 'report_type': 'weekly', 'description': 'Overall node health metrics for the past 7 days. 98.5% uptime achieved across all nodes.'},
            {'title': 'Monthly Detection Summary', 'report_type': 'monthly', 'description': 'Analysis of 142,567 detections across 45 cameras. Peak hours: 8AM-10AM and 5PM-7PM.'},
            {'title': 'Daily Performance Snapshot', 'report_type': 'daily', 'description': 'Real-time performance metrics. Average latency: 23ms. No critical incidents.'},
        ]
        AnalyticsReport.objects.all().delete()
        for r in reports_data:
            AnalyticsReport.objects.create(**r)

        # Edge Nodes
        locations = [
            ('IIIT Kottayam Gate', 9.945, 76.572),
            ('Admin Block', 9.946, 76.573),
            ('Library Wing', 9.947, 76.571),
            ('Hostel Block A', 9.944, 76.570),
            ('Parking Lot North', 9.948, 76.574),
            ('Main Road Junction', 9.943, 76.569),
            ('Sports Complex', 9.949, 76.575),
            ('Cafeteria', 9.946, 76.572),
        ]
        EdgeNode.objects.all().delete()
        for i, (loc, lat, lng) in enumerate(locations, 1):
            status = random.choice(['online', 'online', 'online', 'online', 'offline', 'error'])
            node = EdgeNode.objects.create(
                node_id=f'EN-{i:03d}',
                name=f'Edge Node {i:03d}',
                location=loc,
                latitude=lat, longitude=lng,
                status=status,
                ip_address=f'192.168.{random.randint(1,10)}.{random.randint(10,254)}',
                cpu_usage=round(random.uniform(15, 95), 1),
                memory_usage=round(random.uniform(20, 88), 1),
                disk_usage=round(random.uniform(25, 82), 1),
                temperature=round(random.uniform(35, 72), 1),
                uptime_hours=round(random.uniform(24, 720), 1),
                firmware_version=f'v2.{random.randint(1,4)}.{random.randint(0,9)}',
            )
            NodeConfiguration.objects.create(
                node=node,
                detection_sensitivity=round(random.uniform(0.5, 0.95), 2),
                frame_rate=random.choice([15, 24, 30, 60]),
                resolution=random.choice(['720p', '1080p', '4K']),
                ai_model=random.choice(['YOLOv8', 'YOLOv9', 'EfficientDet']),
            )
            # Node logs
            levels = ['info', 'info', 'info', 'warning', 'error', 'debug']
            log_msgs = [
                'Detection pipeline initialized successfully',
                'Frame buffer cleared, processing resumed',
                'Connection to cloud relay restored',
                'Memory pressure detected, cache cleared',
                'GPU temperature spike detected: 78°C',
                'Model inference: avg 12ms per frame',
                'Alert threshold exceeded for zone 3',
                'Firmware auto-update check completed',
                'Network latency spike: 150ms to relay',
                'Object tracking: 24 active targets',
            ]
            for j in range(random.randint(5, 15)):
                NodeLog.objects.create(
                    node=node,
                    level=random.choice(levels),
                    message=random.choice(log_msgs),
                    source=f'Module-{random.choice(["detector", "tracker", "relay", "core"])}',
                    timestamp=timezone.now() - timedelta(hours=random.randint(0, 48)),
                )

        # Vehicles
        Vehicle.objects.all().delete()
        plates = ['KL-07-AX-1234', 'KL-07-BW-5678', 'TN-01-AB-9012', 'KA-05-CD-3456',
                  'KL-08-EF-7890', 'MH-12-GH-2345', 'KL-07-IJ-6789', 'DL-04-KL-0123']
        types = ['car', 'car', 'truck', 'bus', 'car', 'motorcycle', 'car', 'truck']
        colors = ['White', 'Silver', 'Red', 'Yellow', 'Black', 'Blue', 'Grey', 'White']
        makes = ['Toyota', 'Hyundai', 'Tata', 'Ashok Leyland', 'Maruti', 'Royal Enfield', 'Honda', 'BharatBenz']
        for i, plate in enumerate(plates):
            flagged = i in [2, 5]
            v = Vehicle.objects.create(
                plate_number=plate, vehicle_type=types[i], color=colors[i],
                make=makes[i], model=f'Model-{random.choice(["A", "B", "C", "X"])}',
                is_flagged=flagged,
                flag_reason='Reported stolen vehicle' if flagged else '',
            )
            nodes_list = EdgeNode.objects.all()
            for _ in range(random.randint(2, 6)):
                n = random.choice(list(nodes_list))
                VehicleDetection.objects.create(
                    vehicle=v, node_name=n.name,
                    confidence=round(random.uniform(0.7, 0.99), 2),
                    latitude=n.latitude + random.uniform(-0.002, 0.002),
                    longitude=n.longitude + random.uniform(-0.002, 0.002),
                    speed=round(random.uniform(0, 60), 1),
                    detected_at=timezone.now() - timedelta(hours=random.randint(0, 72)),
                )

        # Training Jobs
        TrainingJob.objects.all().delete()
        jobs_data = [
            {'name': 'Vehicle Detection v3', 'model_type': 'YOLOv8', 'dataset': 'campus-vehicles-v2', 'status': 'completed', 'epochs': 100, 'current_epoch': 100, 'accuracy': 94.2, 'loss': 0.0312, 'training_time': 3600},
            {'name': 'Person Re-ID Model', 'model_type': 'ResNet50', 'dataset': 'person-reid-v1', 'status': 'running', 'epochs': 200, 'current_epoch': 142, 'accuracy': 87.5, 'loss': 0.0891, 'training_time': 5200},
            {'name': 'License Plate OCR', 'model_type': 'EfficientDet', 'dataset': 'plates-indian-v3', 'status': 'completed', 'epochs': 50, 'current_epoch': 50, 'accuracy': 96.8, 'loss': 0.0187, 'training_time': 1800},
            {'name': 'Anomaly Detection v2', 'model_type': 'YOLOv9', 'dataset': 'anomaly-campus', 'status': 'failed', 'epochs': 150, 'current_epoch': 67, 'accuracy': 45.3, 'loss': 1.234, 'training_time': 2400},
        ]
        for jd in jobs_data:
            job = TrainingJob.objects.create(**jd)
            Hyperparameter.objects.create(job=job, name='learning_rate', value=str(round(random.uniform(0.0001, 0.01), 4)))
            Hyperparameter.objects.create(job=job, name='batch_size', value=str(random.choice([8, 16, 32, 64])))
            Hyperparameter.objects.create(job=job, name='optimizer', value=random.choice(['Adam', 'SGD', 'AdamW']))
            # Training logs
            log_msgs_train = [
                'Epoch started, loading batch data...',
                'Forward pass completed, computing gradients...',
                'Backward pass completed, updating weights...',
                'Validation accuracy improved, saving checkpoint...',
                'Learning rate adjusted by scheduler',
                'GPU memory: 6.2GB / 8.0GB used',
                'Data augmentation pipeline active',
                'Early stopping patience: 8/10',
            ]
            for k in range(random.randint(8, 20)):
                TrainingLog.objects.create(
                    job=job,
                    level=random.choice(['info', 'info', 'warning', 'debug']),
                    message=random.choice(log_msgs_train),
                    epoch=random.randint(1, jd['current_epoch']) if jd['current_epoch'] > 0 else None,
                )

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
