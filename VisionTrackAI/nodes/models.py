from django.db import models


class EdgeNode(models.Model):
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('maintenance', 'Maintenance'),
        ('error', 'Error'),
    ]
    node_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='online')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    cpu_usage = models.FloatField(default=0)
    memory_usage = models.FloatField(default=0)
    disk_usage = models.FloatField(default=0)
    temperature = models.FloatField(default=0)
    uptime_hours = models.FloatField(default=0)
    firmware_version = models.CharField(max_length=50, blank=True)
    last_seen = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.node_id})"


class NodeConfiguration(models.Model):
    node = models.OneToOneField(EdgeNode, on_delete=models.CASCADE, related_name='configuration')
    detection_sensitivity = models.FloatField(default=0.7)
    frame_rate = models.IntegerField(default=30)
    resolution = models.CharField(max_length=20, default='1080p')
    ai_model = models.CharField(max_length=100, default='YOLOv8')
    recording_enabled = models.BooleanField(default=True)
    alert_threshold = models.FloatField(default=0.8)
    auto_restart = models.BooleanField(default=True)
    config_json = models.JSONField(default=dict)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Config for {self.node.name}"


class NodeConfigHistory(models.Model):
    node = models.ForeignKey(EdgeNode, on_delete=models.CASCADE, related_name='config_history')
    field_changed = models.CharField(max_length=100)
    old_value = models.CharField(max_length=200)
    new_value = models.CharField(max_length=200)
    changed_by = models.CharField(max_length=100)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.node.name} - {self.field_changed}"


class NodeLog(models.Model):
    LOG_LEVEL_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('debug', 'Debug'),
    ]
    node = models.ForeignKey(EdgeNode, on_delete=models.CASCADE, related_name='logs')
    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES, default='info')
    message = models.TextField()
    source = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.level}] {self.node.name}: {self.message[:50]}"
