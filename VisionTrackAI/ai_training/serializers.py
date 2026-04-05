from rest_framework import serializers
from .models import TrainingJob, TrainingLog, HyperparameterComparison


class TrainingJobSerializer(serializers.ModelSerializer):
    progress = serializers.ReadOnlyField()

    class Meta:
        model = TrainingJob
        fields = '__all__'


class TrainingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingLog
        fields = '__all__'


class HyperparameterComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HyperparameterComparison
        fields = '__all__'
