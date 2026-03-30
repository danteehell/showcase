from django.contrib import admin
from .models import Task, TaskCategory, TaskSkill


class TaskCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name", "slug")
    list_display_links = ("name",)
    list_editable = ("slug",)


class SkillInline(admin.TabularInline):
    model = TaskSkill
    extra = 1
    fields = ("skill", "level_required")


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "deadline", "difficulty", "status")
    list_filter = ("status", "difficulty", "deadline")
    list_display_links = ("title",)
    search_fields = ("title", "project__title")
    list_editable = ("status", "deadline")
    list_per_page = 15
    autocomplete_fields = ("project", "category")

    inlines = (SkillInline,)

    fieldsets = (
        ("Основная информация о задаче", {
            "fields": (
                "title",
                "short_description",
                "description"
            )
        }),
        ("Категория и проект", {
            "fields": (
                "project",
                "category",
            )
        }),
        ("Характеристики задачи", {
            "fields": (
                "difficulty",
                "points",
                "deadline",
                "status"
            )
        }),
    )


admin.site.register(Task, TaskAdmin)
admin.site.register(TaskCategory, TaskCategoryAdmin)