from django.contrib import admin
from .models import TrainingJob, TrainingLog, Hyperparameter, HyperparameterComparison

@admin.register(TrainingJob)
class TrainingJobAdmin(admin.ModelAdmin):
    list_display = ('name', 'model_type', 'status', 'accuracy', 'loss', 'current_epoch', 'epochs')

@admin.register(TrainingLog)
class TrainingLogAdmin(admin.ModelAdmin):
    list_display = ('job', 'level', 'message', 'timestamp')

@admin.register(Hyperparameter)
class HyperparameterAdmin(admin.ModelAdmin):
    list_display = ('job', 'name', 'value')

@admin.register(HyperparameterComparison)
class HyperparameterComparisonAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_saved', 'created_at')
