from django.contrib import admin
from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'department', 'project_lead', 'deadline', 'created_at')
    list_filter = ('department', 'deadline', 'created_at')
    search_fields = ('project_name', 'description')
    filter_horizontal = ('members',)
    date_hierarchy = 'deadline'
