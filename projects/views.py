from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.db import models as django_models
from .models import Project

@login_required
def projects_list(request):
    """Display projects accessible to the logged-in user"""
    user = request.user
    
    if user.role == 'admin':
        # Admin can see all projects
        projects = Project.objects.all()
    elif user.role == 'dept_head':
        # Department head can see all projects in their department
        if user.department:
            projects = Project.objects.filter(department=user.department)
        else:
            projects = Project.objects.none()
    else:
        # Project leads and members see projects they're involved in
        projects = Project.objects.filter(
            django_models.Q(project_lead=user) | django_models.Q(members=user)
        ).distinct()
    
    projects = projects.order_by('-created_at')
    
    # Add member count for each project
    for project in projects:
        project.members_count = project.members.count()
    
    context = {
        'projects': projects,
    }
    return render(request, 'projects/list.html', context)

@login_required
def project_detail(request, project_id):
    """Display project details"""
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    
    # Check access permissions
    has_access = False
    
    if user.role == 'admin':
        has_access = True
    elif user.role == 'dept_head' and user.department == project.department:
        has_access = True
    elif project.project_lead == user:
        has_access = True
    elif user in project.members.all():
        has_access = True
    
    if not has_access:
        raise Http404("You don't have permission to view this project.")
    
    members = project.members.all().order_by('username')
    tasks = project.tasks.all().order_by('-created_at')
    
    context = {
        'project': project,
        'members': members,
        'tasks': tasks,
        'members_count': members.count(),
        'tasks_count': tasks.count(),
    }
    return render(request, 'projects/detail.html', context)
