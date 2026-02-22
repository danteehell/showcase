from django.contrib import admin
from .models import *

admin.site.site_header = "Управление проектами"

class ProjectListItemInline(admin.TabularInline):
    model = ProjectListItem
    extra = 1
    autocomplete_fields = ("project",)
    fields = ("type", "position", "text")
    ordering = ("position",)

class FilterOptionInline(admin.TabularInline):
    model = FilterOption
    extra = 1
    fields = ("name",)
    show_change_link = True

class CampusAdmin(admin.ModelAdmin):
    list_display = ("name","abbreviation","metro_station")
    search_fields = ("name","address","abbreviation")
    list_filter = ("metro_station",)
    ordering = ("name",)
    fieldsets = ((None,{"fields":("name","abbreviation")}),("Контакты",{"fields":("address","metro_station"),"classes":("collapse",)}),)

class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name","website","email","phone","internship")
    search_fields = ("name","email","phone")
    list_filter = ("internship",)
    ordering = ("name",)
    fieldsets = ((None,{"fields":("name","website")}),("Контакты",{"fields":("email","phone"),"classes":("collapse",)}),("Дополнительно",{"fields":("internship",),"classes":("collapse",)}),)

class CuratorAdmin(admin.ModelAdmin):
    list_display = ("first_name","last_name","email")
    search_fields = ("first_name","last_name","email")
    ordering = ("last_name","first_name")

class FilterCategoryAdmin(admin.ModelAdmin):
    list_display = ("name","category_type")
    search_fields = ("name",)
    list_filter = ("category_type",)
    inlines = [FilterOptionInline]
    ordering = ("name",)

class FilterOptionAdmin(admin.ModelAdmin):
    list_display = ("name","category")
    search_fields = ("name","category__name")
    list_filter = ("category",)
    autocomplete_fields = ("category",)
    ordering = ("category__name","name")

class ScheduleItemAdmin(admin.ModelAdmin):
    list_display = ("day_of_week","start_time","end_time","note")
    list_filter = ("day_of_week",)
    search_fields = ("note",)
    ordering = ("day_of_week","start_time")

class CourseYearAdmin(admin.ModelAdmin):
    list_display = ("year",)
    search_fields = ("year",)
    ordering = ("year",)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title","partner","curator","difficulty","spots_remaining","internship","is_active")
    list_filter = ("is_active","internship","difficulty","campus","partner","curator")
    search_fields = ("title","short_description","long_description")
    autocomplete_fields = ("theme","campus","difficulty","partner","curator","specialties","courses")
    list_editable = ("spots_remaining","internship","is_active")
    ordering = ("-created_at",)
    inlines = [ProjectListItemInline]

    fieldsets = (
        ("Основная информация",{"fields":("title","short_description","long_description")}),
        ("Фильтры",{"fields":("theme","specialties","campus","courses","difficulty")}),
        ("Партнёры и кураторы",{"fields":("partner","curator","internship")}),
        ("Доступность",{"fields":("spots_remaining","is_active")}),
    )

admin.site.register(Campus,CampusAdmin)
admin.site.register(Partner,PartnerAdmin)
admin.site.register(Curator,CuratorAdmin)
admin.site.register(FilterCategory,FilterCategoryAdmin)
admin.site.register(FilterOption,FilterOptionAdmin)
admin.site.register(ScheduleItem,ScheduleItemAdmin)
admin.site.register(CourseYear,CourseYearAdmin)
admin.site.register(Project,ProjectAdmin)