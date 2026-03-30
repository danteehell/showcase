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