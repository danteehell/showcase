from django.urls import path
from .views import *

urlpatterns = [
    path('projects', ProjectListAPI.as_view(), name='project-list'),
    path('projects/<int:id>/', ProjectDetailAPI.as_view(), name='project-detail'),
    path('filters', FiltersAPI.as_view(), name='filters'),
    path('partners', PartnerAPI.as_view(), name='partners')
]