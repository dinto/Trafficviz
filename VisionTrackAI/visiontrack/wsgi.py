"""
WSGI config for visiontrack project.
"""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visiontrack.settings')
application = get_wsgi_application()
