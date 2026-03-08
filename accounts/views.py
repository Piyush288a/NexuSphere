from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from departments.models import Department
from projects.models import Project
from tasks.models import Task
from chat.models import Message
from accounts.models import User

def custom_login(request):
    if request.user.is_authenticated:
        return redirect_by_role(request.user)
    
    if request.method == 'POST':
        workspace_code = request.POST.get('workspace_code', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Check if workspace exists
        try:
            department = Department.objects.get(workspace_code=workspace_code)
        except Department.DoesNotExist:
            messages.error(request, 'Workspace not found.')
            return render(request, 'registration/login.html', {
                'workspace_code': workspace_code,
                'username': username,
                'debug': settings.DEBUG
            })
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Check if user's department matches workspace
            if user.department == department:
                login(request, user)
                return redirect_by_role(user)
            else:
                messages.error(request, 'Invalid workspace for this user.')
                return render(request, 'registration/login.html', {
                    'workspace_code': workspace_code,
                    'username': username,
                    'debug': settings.DEBUG
                })
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'registration/login.html', {
                'workspace_code': workspace_code,
                'username': username,
                'debug': settings.DEBUG
            })
    
    return render(request, 'registration/login.html', {'debug': settings.DEBUG})

def custom_logout(request):
    logout(request)
    return redirect('login')

def redirect_by_role(user):
    """Redirect user based on their role"""
    role_redirects = {
        'admin': 'admin_dashboard',
        'dept_head': 'department_dashboard',
        'project_lead': 'project_dashboard',
        'member': 'dashboard',
    }
    return redirect(role_redirects.get(user.role, 'dashboard'))

@login_required
def dashboard(request):
    context = {
        'departments_count': Department.objects.count(),
        'projects_count': Project.objects.count(),
        'tasks_count': Task.objects.count(),
        'messages_count': Message.objects.count(),
        'my_tasks': Task.objects.filter(assigned_to=request.user)[:5],
        'recent_projects': Project.objects.all().order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)

@login_required
def admin_dashboard(request):
    context = {
        'user': request.user,
        'workspace': request.user.department.department_name if request.user.department else 'No Workspace',
        'workspace_code': request.user.department.workspace_code if request.user.department else 'N/A',
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

@login_required
def department_dashboard(request):
    context = {
        'user': request.user,
        'workspace': request.user.department.department_name if request.user.department else 'No Workspace',
        'workspace_code': request.user.department.workspace_code if request.user.department else 'N/A',
    }
    return render(request, 'dashboards/department_dashboard.html', context)

@login_required
def project_dashboard(request):
    context = {
        'user': request.user,
        'workspace': request.user.department.department_name if request.user.department else 'No Workspace',
        'workspace_code': request.user.department.workspace_code if request.user.department else 'N/A',
    }
    return render(request, 'dashboards/project_dashboard.html', context)
