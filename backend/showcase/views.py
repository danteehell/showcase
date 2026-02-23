from django.http import JsonResponse
from .models import FilterCategory, FilterOption, Project, Partner, Curator, Campus
from django.core import serializers
import json

def project_list_api(request):
    projects = Project.objects.all()
    
    data = []
    for project in projects:
        data.append({
            'id': project.id,
            'title': project.title,
            'theme': project.theme.name if project.theme else None,
            'specialties': [s.name for s in project.specialties.all()],
            'campus': project.campus.name if project.campus else None,
            'courses': [c.name for c in project.courses.all()],
            'difficulty': project.difficulty.name if project.difficulty else None,
            'partner': project.partner.name if project.partner else None,
            'curator': project.curator.name if project.curator else None,
            'internship': project.internship,
            'spots_remaining': project.spots_remaining,
            'short_description': project.short_description,
            'long_description': project.long_description,
            'is_active': project.is_active,
            'created_at': project.created_at,
            'updated_at': project.updated_at,
        })
    
    return JsonResponse({'projects': data}, safe=False)

def filters_api(request):
    categories = FilterCategory.objects.all().prefetch_related('options')
    
    data = {}
    for category in categories:
        data[category.category_type] = {
            'id': category.id,
            'name': category.name,
            'options': [
                {'id': opt.id, 'name': opt.name}
                for opt in category.options.all()
            ]
        }
    
    #return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    return JsonResponse(data)