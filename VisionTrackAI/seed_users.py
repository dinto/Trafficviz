import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visiontrack.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile, AccessRequest
from django.utils import timezone

demo_users = [
    {'username':'sarah_connor','email':'s.connor@sky.net','first_name':'Sarah','last_name':'Connor','role':'operator','org':'Skynet Corp','verified':True},
    {'username':'john_wick','email':'j.wick@continental.io','first_name':'John','last_name':'Wick','role':'analyst','org':'Continental','verified':True},
    {'username':'marcus_a','email':'marcus@empire.gov','first_name':'Marcus','last_name':'Aurelius','role':'viewer','org':'Empire Security','verified':True},
    {'username':'alex_rivers','email':'alex.rivers@surv-ops.net','first_name':'Alex','last_name':'Rivers','role':'viewer','org':'Surv Ops','verified':False},
    {'username':'jordan_smith','email':'j.smith@security-ai.io','first_name':'Jordan','last_name':'Smith','role':'viewer','org':'Security AI','verified':False},
    {'username':'david_chen','email':'d.chen@visiontrack.io','first_name':'David','last_name':'Chen','role':'admin','org':'VisionTrackAI','verified':True},
]

created = 0
for u in demo_users:
    if not User.objects.filter(username=u['username']).exists():
        user = User.objects.create_user(
            username=u['username'], email=u['email'], password='demo123',
            first_name=u['first_name'], last_name=u['last_name']
        )
        UserProfile.objects.create(
            user=user, role=u['role'], organization=u['org'],
            is_verified=u['verified'], phone='555-0100'
        )
        created += 1

# Create pending access requests for alex and jordan
for uname, role in [('alex_rivers', 'operator'), ('jordan_smith', 'analyst')]:
    user = User.objects.get(username=uname)
    if not AccessRequest.objects.filter(user=user, status='pending').exists():
        AccessRequest.objects.create(
            user=user, requested_role=role,
            reason='Need elevated access for monitoring duties.',
            status='pending'
        )

# Create approved request for sarah
user = User.objects.get(username='sarah_connor')
if not AccessRequest.objects.filter(user=user, status='approved').exists():
    admin = User.objects.get(username='admin')
    AccessRequest.objects.create(
        user=user, requested_role='operator',
        reason='Promoted to operator role.',
        status='approved', reviewed_by=admin, reviewed_at=timezone.now()
    )

# Ensure admin user has a profile
admin_user = User.objects.get(username='admin')
if not hasattr(admin_user, 'profile') or not UserProfile.objects.filter(user=admin_user).exists():
    UserProfile.objects.get_or_create(
        user=admin_user,
        defaults={'role': 'admin', 'organization': 'VisionTrackAI', 'is_verified': True}
    )

print(f'Created {created} demo users')
print(f'Total users: {User.objects.count()}')
print(f'Pending requests: {AccessRequest.objects.filter(status="pending").count()}')
