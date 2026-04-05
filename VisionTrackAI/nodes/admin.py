from django.contrib import admin
from .models import EdgeNode, NodeConfiguration, NodeConfigHistory, NodeLog

@admin.register(EdgeNode)
class EdgeNodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'node_id', 'location', 'status', 'cpu_usage', 'memory_usage', 'last_seen')

@admin.register(NodeConfiguration)
class NodeConfigurationAdmin(admin.ModelAdmin):
    list_display = ('node', 'ai_model', 'resolution', 'frame_rate', 'recording_enabled')

@admin.register(NodeConfigHistory)
class NodeConfigHistoryAdmin(admin.ModelAdmin):
    list_display = ('node', 'field_changed', 'old_value', 'new_value', 'changed_by', 'changed_at')

@admin.register(NodeLog)
class NodeLogAdmin(admin.ModelAdmin):
    list_display = ('node', 'level', 'message', 'timestamp')
