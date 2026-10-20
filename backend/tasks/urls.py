from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'tasks', TasksView, basename='tasks')

urlpatterns = [
    path('', include(router.urls)),
    
    path('filters/', TaskFiltersAPIView.as_view(), name='task-filters')
]
