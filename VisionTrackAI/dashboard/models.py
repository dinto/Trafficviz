from django.db import models
import json


class DashboardMetric(models.Model):
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    unit = models.CharField(max_length=20, blank=True)
    icon = models.CharField(max_length=50, default='activity')
    change_percent = models.FloatField(default=0)
    is_positive = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.name}: {self.value}"


class Alert(models.Model):
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]
    title = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info')
    source = models.CharField(max_length=100, blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.severity}] {self.title}"


class AnalyticsReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('custom', 'Custom'),
    ]
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='daily')
    description = models.TextField(blank=True)
    data_json = models.JSONField(default=dict)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return self.title


class AIQueryLog(models.Model):
    query = models.TextField()
    response = models.TextField()
    confidence = models.FloatField(default=0)
    image_type = models.CharField(max_length=30, blank=True, default='')
    map_data = models.JSONField(blank=True, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.query[:50]

    @property
    def map_data_json(self):
        if self.map_data:
            return json.dumps(self.map_data)
        return ''
