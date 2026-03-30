from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from .models import *
from .serializers import TasksSerializer


class TasksView(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.select_related("project", "category").all()
    serializer_class = TasksSerializer
    permission_classes = [AllowAny]