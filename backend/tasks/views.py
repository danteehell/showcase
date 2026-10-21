from django.db.models import Min, Max
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Task, TaskCategory
from showcase.models import Project
from .serializers import TaskListSerializer, TaskDetailSerializer


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Task.objects.select_related("project", "category").filter(
            status__in=[
                Task.Status.PUBLISHED,
                Task.Status.TAKEN,
                Task.Status.IN_PROGRESS,
            ]
        )

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskListSerializer


class TaskFiltersAPIView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = list(
            TaskCategory.objects.values('id', 'name', 'slug')
        )
        projects = list(
            Project.objects.values('id', 'title')
        )
        points = Task.objects.aggregate(
            points_min=Min('points'), points_max=Max('points'),
        )
        deadlines = Task.objects.aggregate(
            deadline_min=Min('deadline'), deadline_max=Max('deadline'),
        )
        difficulties = [choice[0] for choice in Task.Difficulty.choices]

        return Response({
            'categories': categories,
            'projects': projects,
            'points_min': points['points_min'] or 0,
            'points_max': points['points_max'] or 0,
            'deadline_min': deadlines['deadline_min'],
            'deadline_max': deadlines['deadline_max'],
            'difficulties': difficulties,
        })