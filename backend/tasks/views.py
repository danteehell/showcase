from django.shortcuts import render
from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import TasksSerializer, TaskFiltersSerializer
from django.db.models import Min, Max


class TasksView(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.select_related("project", "category").all()
    serializer_class = TasksSerializer
    permission_classes = [AllowAny]


class TaskFiltersAPIView(views.APIView):

    def get(self, request, *args, **kwargs):

        categories_qs = TaskCategory.objects.all()
        categories = [{'id': c.id, 'name': c.name, 'slug': c.slug} for c in categories_qs]

        projects_qs = Task.objects.select_related('project').values('project__id', 'project__name')

        projects = [{'id': p["project__id"], 'name': p['project__name']} for p in projects_qs]

        points = Task.objects.aggregate(points_min=Min('points'), points_max=Max('points'))

        deadlines = Task.objects.aggregate(deadline_min=Min('deadline'), deadline_max=Max('deadline'))

        difficulties = [choice[0] for choice in Task.Difficulty.choices]

        data = {
            'categories': categories,
            'projects': projects,
            'points_min': points['points_min'] or 0,
            'points_max': points['points_max'] or 0,
            'deadline_min': deadlines['deadline_min'],
            'deadline_max': deadlines['deadline_max'],
            'difficulties': difficulties,
        }

        serializer = TaskFiltersSerializer(data)
        return Response(serializer.data)