from rest_framework import serializers
from .models import DashboardMetric, Alert, AnalyticsReport


class DashboardMetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardMetric
        fields = '__all__'


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class AnalyticsReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsReport
        fields = '__all__'
