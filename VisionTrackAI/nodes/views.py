from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework import viewsets
from .models import EdgeNode, NodeConfiguration, NodeConfigHistory, NodeLog
from .serializers import EdgeNodeSerializer, NodeConfigSerializer, NodeLogSerializer
import csv


@login_required
def node_list(request):
    nodes = EdgeNode.objects.all()
    status_filter = request.GET.get('status')
    search = request.GET.get('search', '')
    if status_filter:
        nodes = nodes.filter(status=status_filter)
    if search:
        nodes = nodes.filter(name__icontains=search)
    context = {
        'nodes': nodes,
        'total': EdgeNode.objects.count(),
        'online': EdgeNode.objects.filter(status='online').count(),
        'offline': EdgeNode.objects.filter(status='offline').count(),
        'error': EdgeNode.objects.filter(status='error').count(),
    }
    return render(request, 'nodes/node_list.html', context)


@login_required
def node_detail(request, pk):
    node = get_object_or_404(EdgeNode, pk=pk)
    config, _ = NodeConfiguration.objects.get_or_create(node=node)
    logs = NodeLog.objects.filter(node=node)
    config_history = NodeConfigHistory.objects.filter(node=node)

    # Filtering
    log_level = request.GET.get('level')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    log_search = request.GET.get('log_search', '')

    if log_level:
        logs = logs.filter(level=log_level)
    if date_from:
        logs = logs.filter(timestamp__date__gte=date_from)
    if date_to:
        logs = logs.filter(timestamp__date__lte=date_to)
    if log_search:
        logs = logs.filter(message__icontains=log_search)

    context = {
        'node': node,
        'config': config,
        'logs': logs[:50],
        'config_history': config_history[:20],
    }
    return render(request, 'nodes/node_detail.html', context)


@login_required
def node_config(request, pk):
    node = get_object_or_404(EdgeNode, pk=pk)
    config, _ = NodeConfiguration.objects.get_or_create(node=node)

    if request.method == 'POST':
        fields = ['detection_sensitivity', 'frame_rate', 'resolution', 'ai_model',
                   'recording_enabled', 'alert_threshold', 'auto_restart']
        for field in fields:
            old_val = str(getattr(config, field))
            new_val = request.POST.get(field, old_val)
            if field == 'recording_enabled':
                new_val = 'on' in str(new_val).lower() or new_val == 'True'
            elif field == 'auto_restart':
                new_val = 'on' in str(new_val).lower() or new_val == 'True'
            elif field in ['detection_sensitivity', 'alert_threshold']:
                new_val = float(new_val)
            elif field == 'frame_rate':
                new_val = int(new_val)
            if str(old_val) != str(new_val):
                NodeConfigHistory.objects.create(
                    node=node, field_changed=field,
                    old_value=old_val, new_value=str(new_val),
                    changed_by=request.user.username
                )
                setattr(config, field, new_val)
        config.save()
        return redirect('nodes:node_detail', pk=pk)

    return render(request, 'nodes/node_config.html', {'node': node, 'config': config})


@login_required
def node_logs_export(request, pk):
    node = get_object_or_404(EdgeNode, pk=pk)
    logs = NodeLog.objects.filter(node=node)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{node.name}_logs.csv"'
    writer = csv.writer(response)
    writer.writerow(['Timestamp', 'Level', 'Message', 'Source'])
    for log in logs:
        writer.writerow([log.timestamp, log.level, log.message, log.source])
    return response


class EdgeNodeViewSet(viewsets.ModelViewSet):
    queryset = EdgeNode.objects.all()
    serializer_class = EdgeNodeSerializer


class NodeLogViewSet(viewsets.ModelViewSet):
    queryset = NodeLog.objects.all()
    serializer_class = NodeLogSerializer
