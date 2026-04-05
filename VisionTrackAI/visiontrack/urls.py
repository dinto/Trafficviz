from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r: redirect('dashboard:home')),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('nodes/', include('nodes.urls')),
    path('vehicles/', include('vehicles.urls')),
    path('ai-training/', include('ai_training.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
