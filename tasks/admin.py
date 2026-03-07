from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assigned_to', 'status', 'priority', 'deadline', 'created_at')
    list_filter = ('status', 'priority', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'deadline'
    list_editable = ('status', 'priority')
