from django.contrib import admin
from .models import DashboardMetric, Alert, AnalyticsReport, AIQueryLog

@admin.register(DashboardMetric)
class DashboardMetricAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'unit', 'change_percent', 'order')

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'severity', 'source', 'is_resolved', 'created_at')

@admin.register(AnalyticsReport)
class AnalyticsReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'report_type', 'generated_at')

@admin.register(AIQueryLog)
class AIQueryLogAdmin(admin.ModelAdmin):
    list_display = ('query', 'confidence', 'created_at')
