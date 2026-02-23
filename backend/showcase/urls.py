from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list_api, name='project-list'),
    path('/filtres', views.filters_api, name='filtres'),
]