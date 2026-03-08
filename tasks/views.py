from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from .models import Task
from projects.models import Project
from .forms import TaskForm, TaskStatusForm


@login_required
def task_list(request, project_id):
    """Display all tasks for a project"""
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
        raise Http404("You don't have permission to view this project's tasks.")
    
    tasks = project.tasks.all().order_by('-created_at')
    
    # Calculate task statistics
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(status='Completed').count()
    in_progress_tasks = tasks.filter(status='In Progress').count()
    pending_tasks = tasks.filter(status='Pending').count()
    
    context = {
        'project': project,
        'tasks': tasks,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'pending_tasks': pending_tasks,
    }
    return render(request, 'tasks/list.html', context)


@login_required
def task_create(request, project_id):
    """Create a new task for a project"""
    project = get_object_or_404(Project, id=project_id)
    user = request.user
    
    # Check if user has permission to create tasks
    can_create = False
    if user.role == 'admin':
        can_create = True
    elif user.role == 'dept_head' and user.department == project.department:
        can_create = True
    elif project.project_lead == user:
        can_create = True
    
    if not can_create:
        messages.error(request, "You don't have permission to create tasks for this project.")
        return redirect('project_detail', project_id=project.id)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, project=project)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f'Task "{task.title}" created successfully!')
            return redirect('task_list', project_id=project.id)
    else:
        form = TaskForm(project=project)
    
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'tasks/create.html', context)


@login_required
def task_detail(request, task_id):
    """Display task details"""
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    
    # Check access permissions
    has_access = False
    if user.role == 'admin':
        has_access = True
    elif user.role == 'dept_head' and user.department == task.project.department:
        has_access = True
    elif task.project.project_lead == user:
        has_access = True
    elif user in task.project.members.all():
        has_access = True
    
    if not has_access:
        raise Http404("You don't have permission to view this task.")
    
    # Check if user can update status
    can_update_status = False
    if user.role == 'admin':
        can_update_status = True
    elif task.project.project_lead == user:
        can_update_status = True
    elif task.assigned_to == user:
        can_update_status = True
    
    context = {
        'task': task,
        'can_update_status': can_update_status,
    }
    return render(request, 'tasks/detail.html', context)


@login_required
def task_update_status(request, task_id):
    """Update task status"""
    task = get_object_or_404(Task, id=task_id)
    user = request.user
    
    # Check if user can update status
    can_update = False
    if user.role == 'admin':
        can_update = True
    elif task.project.project_lead == user:
        can_update = True
    elif task.assigned_to == user:
        can_update = True
    
    if not can_update:
        messages.error(request, "You don't have permission to update this task.")
        return redirect('task_detail', task_id=task.id)
    
    if request.method == 'POST':
        form = TaskStatusForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task status updated to "{task.status}"!')
            return redirect('task_detail', task_id=task.id)
    
    return redirect('task_detail', task_id=task.id)
