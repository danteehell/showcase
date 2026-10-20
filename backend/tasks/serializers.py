from rest_framework import serializers
from .models import Task

class TasksSerializer(serializers.ModelSerializer):
    project = serializers.CharField(source="project.title", read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'project',
            'short_description',
            'description',
            'category',
            'difficulty',
            'points',
            'deadline',
            'status',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_category(self, obj):
        return obj.category.name if obj.category else None


class TaskFiltersSerializer(serializers.Serializer):
    categories = serializers.ListField()
    projects = serializers.ListField()
    points_min = serializers.DecimalField(max_digits=6, decimal_places=2)
    points_max = serializers.DecimalField(max_digits=6, decimal_places=2)
    deadline_min = serializers.DateTimeField()
    deadline_max = serializers.DateTimeField()
    difficulties = serializers.ListField()
