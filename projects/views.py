from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.contrib import messages
from django.db import models as django_models
from .models import Project
from .forms import ProjectForm

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


@login_required
def project_create(request):
    """Create a new project"""
    user = request.user
    
    # Check if user has permission to create projects
    if user.role not in ['admin', 'dept_head', 'project_lead']:
        messages.error(request, "You don't have permission to create projects.")
        return redirect('projects_list')
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, user=user)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.project_name}" created successfully!')
            return redirect('project_detail', project_id=project.id)
    else:
        form = ProjectForm(user=user)
    
    context = {
        'form': form,
    }
    return render(request, 'projects/create.html', context)
