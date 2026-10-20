from django.urls import path, include
from rest_framework import routers
from .views import ProjectListAPI, ProjectViewSet, FiltersViewSet, PartnerViewSet

router = routers.DefaultRouter()
router.register(r'projects-viewset', ProjectViewSet, basename='project-detail')
router.register(r'filters', FiltersViewSet, basename='filters')
router.register(r'partners', PartnerViewSet, basename='partners')

urlpatterns = [
    path('projects/', ProjectListAPI.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectViewSet.as_view({'get': 'retrieve'}), name='project-detail'),
    path('', include(router.urls)),
]