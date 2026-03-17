from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.shortcuts import get_object_or_404


class ProjectListAPI(APIView):
    def get(self, request, format=None):
        projects = Project.objects.all()

        search = request.GET.get('search')
        if search:
            projects = projects.filter(title__icontains=search)

        theme_ids = request.GET.getlist('theme')
        if theme_ids:
            theme_ids = [int(t) for t in theme_ids]
            projects = projects.filter(theme_id__in=theme_ids)

        difficulty_ids = request.GET.getlist('difficulty')
        if difficulty_ids:
            difficulty_ids = [int(d) for d in difficulty_ids]
            projects = projects.filter(difficulty_id__in=difficulty_ids)

        partner_ids = request.GET.getlist('partner')
        if partner_ids:
            partner_ids = [int(p) for p in partner_ids]
            projects = projects.filter(partner_id__in=partner_ids)

        campus_ids = request.GET.getlist('campus')
        if campus_ids:
            campus_ids = [int(c) for c in campus_ids]
            projects = projects.filter(campus__id__in=campus_ids)

        internship = request.GET.get('internship')
        if internship is not None:
            if internship.lower() in ['true', '1']:
                projects = projects.filter(internship=True)
            elif internship.lower() in ['false', '0']:
                projects = projects.filter(internship=False)

        sort = request.GET.get('sort')
        if sort == 'created_at_desc':
            projects = projects.order_by('-created_at')
        elif sort == 'created_at_asc':
            projects = projects.order_by('created_at')
        elif sort == 'title_asc':
            projects = projects.order_by('title')
        elif sort == 'title_desc':
            projects = projects.order_by('-title')

        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))
        start = (page - 1) * limit
        end = start + limit
        total_projects = projects.count()
        projects_page = projects[start:end]

        serializer = ProjectSerializer(projects_page, many=True)
        return Response({
            'data': serializer.data,
            'totalProjects': total_projects,
            'availableProjects': projects.filter(spots_remaining__gt=0).count(),
            'totalPages': (total_projects + limit - 1) // limit,
            'page': page,
        })

class ProjectDetailAPI(APIView):
    def get(self, reques, id, format=None):
        project = get_object_or_404(Project, id=id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

class FiltersAPI(APIView):
    def get(self, request, format=None):
        categories = FilterCategory.objects.all().prefetch_related('options')
        serializer = FilterCategorySerializer(categories, many=True)
        data = {cat['category_type']: cat for cat in serializer.data}
        return Response(data)
    

class PartnerAPI(APIView):
    def get(self, request, format=None):
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True)
        data = serializer.data
        return Response({"data": data})