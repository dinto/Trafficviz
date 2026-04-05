from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'ai_training'

router = DefaultRouter()
router.register(r'jobs', views.TrainingJobViewSet)
router.register(r'logs', views.TrainingLogViewSet)

urlpatterns = [
    path('', views.training_list, name='training_list'),
    path('<int:pk>/logs/', views.training_logs, name='training_logs'),
    path('comparison/', views.comparison_view, name='comparison'),
    path('comparison/history/', views.comparison_history, name='comparison_history'),
    path('datasets/', views.dataset_upload, name='dataset_upload'),
    path('datasets/<int:pk>/', views.dataset_detail, name='dataset_detail'),
    path('datasets/<int:pk>/train/', views.dataset_train, name='dataset_train'),
    path('datasets/<int:pk>/query/', views.dataset_query, name='dataset_query'),
    path('api/', include(router.urls)),
]
