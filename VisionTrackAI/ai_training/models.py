from django.db import models


class TrainingJob(models.Model):
    STATUS_CHOICES = [
        ('queued', 'Queued'),
        ('running', 'Running'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    name = models.CharField(max_length=200)
    model_type = models.CharField(max_length=100, default='YOLOv8')
    dataset = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='queued')
    epochs = models.IntegerField(default=100)
    current_epoch = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    loss = models.FloatField(default=0)
    training_time = models.FloatField(default=0)
    config_json = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.status})"

    @property
    def progress(self):
        if self.epochs == 0:
            return 0
        return round((self.current_epoch / self.epochs) * 100, 1)


class TrainingLog(models.Model):
    LOG_LEVEL_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('debug', 'Debug'),
    ]
    job = models.ForeignKey(TrainingJob, on_delete=models.CASCADE, related_name='logs')
    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES, default='info')
    message = models.TextField()
    epoch = models.IntegerField(null=True, blank=True)
    metrics_json = models.JSONField(default=dict, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"[{self.level}] {self.job.name}: {self.message[:50]}"


class Hyperparameter(models.Model):
    job = models.ForeignKey(TrainingJob, on_delete=models.CASCADE, related_name='hyperparameters')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name}: {self.value}"


class HyperparameterComparison(models.Model):
    title = models.CharField(max_length=200)
    jobs = models.ManyToManyField(TrainingJob, related_name='comparisons')
    notes = models.TextField(blank=True)
    is_saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TrainingDataset(models.Model):
    STATUS_CHOICES = [
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('ready', 'Ready'),
        ('training', 'Training'),
        ('trained', 'Trained'),
        ('failed', 'Failed'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='uploading')
    model_type = models.CharField(max_length=100, default='YOLOv8')
    total_videos = models.IntegerField(default=0)
    total_frames = models.IntegerField(default=0)
    train_split = models.FloatField(default=0.8)
    test_split = models.FloatField(default=0.2)
    accuracy = models.FloatField(default=0)
    precision_val = models.FloatField(default=0)
    recall_val = models.FloatField(default=0)
    f1_score = models.FloatField(default=0)
    training_job = models.ForeignKey(TrainingJob, on_delete=models.SET_NULL, null=True, blank=True, related_name='datasets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.status})"


class DatasetVideo(models.Model):
    dataset = models.ForeignKey(TrainingDataset, on_delete=models.CASCADE, related_name='videos')
    file = models.FileField(upload_to='training_videos/')
    filename = models.CharField(max_length=255)
    file_size = models.BigIntegerField(default=0)
    duration = models.FloatField(default=0, help_text='Duration in seconds')
    frame_count = models.IntegerField(default=0)
    resolution = models.CharField(max_length=20, blank=True)
    is_processed = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']

    def __str__(self):
        return self.filename

    @property
    def file_size_display(self):
        if self.file_size > 1_000_000_000:
            return f"{self.file_size / 1_000_000_000:.1f} GB"
        elif self.file_size > 1_000_000:
            return f"{self.file_size / 1_000_000:.1f} MB"
        return f"{self.file_size / 1_000:.1f} KB"


class TrainingQuery(models.Model):
    dataset = models.ForeignKey(TrainingDataset, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    result_json = models.JSONField(default=dict)
    confidence = models.FloatField(default=0)
    processing_time = models.FloatField(default=0, help_text='Time in seconds')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Query: {self.query_text[:50]}"

