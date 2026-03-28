from django.contrib import admin
from .models import Project, ProjectProposal


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'department', 'project_lead', 'deadline', 'created_at')
    list_filter = ('department', 'deadline', 'created_at')
    search_fields = ('project_name', 'description')
    filter_horizontal = ('members',)
    date_hierarchy = 'deadline'


@admin.register(ProjectProposal)
class ProjectProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'proposed_by', 'status', 'created_at')
    list_filter = ('status', 'department', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'approved_at', 'rejected_at', 'created_project')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Proposal Information', {
            'fields': ('title', 'description', 'department', 'proposed_by')
        }),
        ('Project Details', {
            'fields': ('proposed_project_lead', 'proposed_deadline')
        }),
        ('Status', {
            'fields': ('status', 'admin_notes', 'created_at', 'approved_at', 'rejected_at')
        }),
        ('Created Project', {
            'fields': ('created_project',),
            'classes': ('collapse',)
        }),
    )
