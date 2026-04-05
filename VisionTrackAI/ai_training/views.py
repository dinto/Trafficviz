from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from rest_framework import viewsets
from .models import (
    TrainingJob, TrainingLog, Hyperparameter, HyperparameterComparison,
    TrainingDataset, DatasetVideo, TrainingQuery
)
from .serializers import TrainingJobSerializer, TrainingLogSerializer, HyperparameterComparisonSerializer
import random
import json


@login_required
def training_list(request):
    jobs = TrainingJob.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        model_type = request.POST.get('model_type', 'YOLOv8')
        dataset = request.POST.get('dataset', '')
        epochs = int(request.POST.get('epochs', 100))
        job = TrainingJob.objects.create(name=name, model_type=model_type, dataset=dataset, epochs=epochs)
        messages.success(request, f'Training job "{name}" created.')
        return redirect('ai_training:training_list')
    return render(request, 'ai_training/training_list.html', {'jobs': jobs})


@login_required
def training_logs(request, pk):
    job = get_object_or_404(TrainingJob, pk=pk)
    logs = TrainingLog.objects.filter(job=job)
    level = request.GET.get('level')
    if level:
        logs = logs.filter(level=level)
    return render(request, 'ai_training/training_logs.html', {'job': job, 'logs': logs})


@login_required
def comparison_view(request):
    jobs = TrainingJob.objects.filter(status='completed')
    selected_ids = request.GET.getlist('jobs')
    selected_jobs = []
    if selected_ids:
        selected_jobs = TrainingJob.objects.filter(pk__in=selected_ids)
    if request.method == 'POST':
        title = request.POST.get('title', 'Comparison')
        job_ids = request.POST.getlist('jobs')
        comp = HyperparameterComparison.objects.create(title=title, is_saved=True)
        comp.jobs.set(job_ids)
        messages.success(request, 'Comparison saved.')
        return redirect('ai_training:comparison_history')
    return render(request, 'ai_training/comparison.html', {'jobs': jobs, 'selected_jobs': selected_jobs})


@login_required
def comparison_history(request):
    comparisons = HyperparameterComparison.objects.filter(is_saved=True)
    return render(request, 'ai_training/comparison_history.html', {'comparisons': comparisons})


class TrainingJobViewSet(viewsets.ModelViewSet):
    queryset = TrainingJob.objects.all()
    serializer_class = TrainingJobSerializer


class TrainingLogViewSet(viewsets.ModelViewSet):
    queryset = TrainingLog.objects.all()
    serializer_class = TrainingLogSerializer


@login_required
def dataset_upload(request):
    datasets = TrainingDataset.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name', 'Unnamed Dataset')
        description = request.POST.get('description', '')
        model_type = request.POST.get('model_type', 'YOLOv8')
        train_split = float(request.POST.get('train_split', 0.8))

        dataset = TrainingDataset.objects.create(
            name=name,
            description=description,
            model_type=model_type,
            train_split=train_split,
            test_split=round(1 - train_split, 2),
        )

        files = request.FILES.getlist('videos')
        for f in files:
            # Simulate video processing
            frame_count = random.randint(300, 5000)
            duration = round(frame_count / 30.0, 1)
            resolutions = ['1920x1080', '1280x720', '640x480', '3840x2160']
            DatasetVideo.objects.create(
                dataset=dataset,
                file=f,
                filename=f.name,
                file_size=f.size,
                duration=duration,
                frame_count=frame_count,
                resolution=random.choice(resolutions),
                is_processed=True,
            )

        dataset.total_videos = len(files)
        dataset.total_frames = sum(v.frame_count for v in dataset.videos.all())
        dataset.status = 'ready'
        dataset.save()

        messages.success(request, f'Dataset "{name}" created with {len(files)} video(s).')
        return redirect('ai_training:dataset_detail', pk=dataset.pk)

    return render(request, 'ai_training/dataset_upload.html', {'datasets': datasets})


@login_required
def dataset_detail(request, pk):
    dataset = get_object_or_404(TrainingDataset, pk=pk)
    videos = dataset.videos.all()
    queries = dataset.queries.all()[:10]
    return render(request, 'ai_training/dataset_detail.html', {
        'dataset': dataset,
        'videos': videos,
        'queries': queries,
    })


@login_required
def dataset_train(request, pk):
    dataset = get_object_or_404(TrainingDataset, pk=pk)
    if request.method == 'POST':
        # Simulate training
        dataset.status = 'trained'
        dataset.accuracy = round(random.uniform(82, 98), 1)
        dataset.precision_val = round(random.uniform(80, 97), 1)
        dataset.recall_val = round(random.uniform(78, 96), 1)
        dataset.f1_score = round(2 * (dataset.precision_val * dataset.recall_val) / (dataset.precision_val + dataset.recall_val), 1)

        # Create a TrainingJob
        job = TrainingJob.objects.create(
            name=f"Train: {dataset.name}",
            model_type=dataset.model_type,
            dataset=dataset.name,
            status='completed',
            epochs=random.randint(50, 200),
            accuracy=dataset.accuracy / 100.0,
            loss=round(random.uniform(0.02, 0.15), 4),
            training_time=round(random.uniform(120, 3600), 1),
        )
        job.current_epoch = job.epochs
        job.save()

        dataset.training_job = job
        dataset.save()

        # Log entries
        for epoch in range(1, min(job.epochs + 1, 6)):
            TrainingLog.objects.create(
                job=job,
                level='info',
                message=f'Epoch {epoch}/{job.epochs} — loss: {round(random.uniform(0.5, 0.02), 4)}, accuracy: {round(random.uniform(0.6, dataset.accuracy), 4)}',
                epoch=epoch,
            )

        messages.success(request, f'Training completed for "{dataset.name}" with {dataset.accuracy * 100:.1f}% accuracy.')
    return redirect('ai_training:dataset_detail', pk=dataset.pk)


@login_required
def dataset_query(request, pk):
    dataset = get_object_or_404(TrainingDataset, pk=pk)
    if request.method == 'POST':
        query_text = request.POST.get('query', '')
        if query_text:
            # Simulate AI inference
            processing_time = round(random.uniform(0.1, 2.5), 3)
            confidence = round(random.uniform(0.72, 0.99), 2)

            # Generate varied result based on query keywords
            query_lower = query_text.lower()
            results = {'query': query_text, 'model': dataset.model_type}

            if any(w in query_lower for w in ['car', 'vehicle', 'truck', 'bus']):
                results['detections'] = [
                    {'type': 'Car', 'count': random.randint(5, 50), 'avg_confidence': round(random.uniform(0.85, 0.98), 2)},
                    {'type': 'Truck', 'count': random.randint(1, 15), 'avg_confidence': round(random.uniform(0.80, 0.95), 2)},
                    {'type': 'Bus', 'count': random.randint(0, 8), 'avg_confidence': round(random.uniform(0.75, 0.92), 2)},
                ]
                results['summary'] = f"Detected {sum(d['count'] for d in results['detections'])} vehicles across {dataset.total_videos} videos."
            elif any(w in query_lower for w in ['speed', 'fast', 'slow']):
                results['speed_analysis'] = {
                    'avg_speed_kmh': round(random.uniform(30, 80), 1),
                    'max_speed_kmh': round(random.uniform(80, 160), 1),
                    'violations': random.randint(0, 12),
                }
                results['summary'] = f"Average speed: {results['speed_analysis']['avg_speed_kmh']} km/h with {results['speed_analysis']['violations']} violations."
            elif any(w in query_lower for w in ['person', 'pedestrian', 'people']):
                results['pedestrian_analysis'] = {
                    'total_detected': random.randint(10, 200),
                    'jaywalking': random.randint(0, 15),
                    'crosswalk_usage': round(random.uniform(0.6, 0.95), 2),
                }
                results['summary'] = f"Detected {results['pedestrian_analysis']['total_detected']} pedestrians."
            elif any(w in query_lower for w in ['traffic', 'congestion', 'flow']):
                results['traffic_flow'] = {
                    'avg_density': round(random.uniform(0.3, 0.9), 2),
                    'peak_hour': f"{random.randint(7, 9)}:00 - {random.randint(17, 19)}:00",
                    'flow_rate': round(random.uniform(500, 2000), 0),
                }
                results['summary'] = f"Traffic density: {results['traffic_flow']['avg_density']:.0%}. Peak: {results['traffic_flow']['peak_hour']}."
            elif any(w in query_lower for w in ['plate', 'number', 'license']):
                plates = [f"KA{random.randint(1,99):02d}{chr(random.randint(65,90))}{chr(random.randint(65,90))}{random.randint(1000,9999)}" for _ in range(random.randint(3, 8))]
                results['plates_detected'] = plates
                results['summary'] = f"Recognized {len(plates)} license plates from video data."
            else:
                results['general_analysis'] = {
                    'objects_detected': random.randint(50, 500),
                    'unique_classes': random.randint(5, 15),
                    'frames_analyzed': dataset.total_frames,
                }
                results['summary'] = f"Analyzed {dataset.total_frames} frames, detected {results['general_analysis']['objects_detected']} objects across {results['general_analysis']['unique_classes']} classes."

            query_obj = TrainingQuery.objects.create(
                dataset=dataset,
                query_text=query_text,
                result_json=results,
                confidence=confidence,
                processing_time=processing_time,
            )
            messages.success(request, f'Query processed in {processing_time}s with {confidence * 100:.0f}% confidence.')
    return redirect('ai_training:dataset_detail', pk=dataset.pk)

