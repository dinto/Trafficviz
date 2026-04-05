from rest_framework import serializers
from .models import EdgeNode, NodeConfiguration, NodeLog


class EdgeNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EdgeNode
        fields = '__all__'


class NodeConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeConfiguration
        fields = '__all__'


class NodeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeLog
        fields = '__all__'
