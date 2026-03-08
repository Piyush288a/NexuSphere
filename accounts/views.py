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
    user = request.user
    
    # My Tasks - assigned to current user
    my_tasks = Task.objects.filter(assigned_to=user).select_related('project', 'project__department')
    
    # Task Statistics
    total_tasks = my_tasks.count()
    completed_tasks = my_tasks.filter(status='Completed').count()
    pending_tasks = my_tasks.filter(status='Pending').count()
    inprogress_tasks = my_tasks.filter(status='In Progress').count()
    
    # Recent tasks (last 10)
    recent_tasks = my_tasks.order_by('-created_at')[:10]
    
    # Upcoming Deadlines - tasks ordered by nearest deadline
    upcoming_deadlines = my_tasks.exclude(status='Completed').order_by('deadline')[:5]
    
    # My Projects - where user is lead or member
    my_projects_as_lead = Project.objects.filter(project_lead=user).select_related('department', 'project_lead')
    my_projects_as_member = Project.objects.filter(members=user).select_related('department', 'project_lead')
    my_projects = (my_projects_as_lead | my_projects_as_member).distinct().order_by('-created_at')[:8]
    
    # Calculate project task progress for each project
    projects_with_progress = []
    for project in my_projects:
        project_tasks = project.tasks.all()
        total_project_tasks = project_tasks.count()
        completed_project_tasks = project_tasks.filter(status='Completed').count()
        progress_percentage = (completed_project_tasks / total_project_tasks * 100) if total_project_tasks > 0 else 0
        
        projects_with_progress.append({
            'project': project,
            'total_tasks': total_project_tasks,
            'completed_tasks': completed_project_tasks,
            'progress_percentage': round(progress_percentage, 1)
        })
    
    context = {
        # Statistics
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        
        # Tasks
        'recent_tasks': recent_tasks,
        'upcoming_deadlines': upcoming_deadlines,
        
        # Projects
        'my_projects': projects_with_progress,
        'projects_count': my_projects.count(),
    }
    return render(request, 'dashboard.html', context)

@login_required
def admin_dashboard(request):
    # Admin sees system-wide statistics
    total_departments = Department.objects.count()
    total_users = User.objects.count()
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    
    # Recent activity
    recent_projects = Project.objects.all().select_related('department', 'project_lead').order_by('-created_at')[:5]
    recent_tasks = Task.objects.all().select_related('project', 'assigned_to').order_by('-created_at')[:10]
    
    # Task statistics
    completed_tasks = Task.objects.filter(status='Completed').count()
    pending_tasks = Task.objects.filter(status='Pending').count()
    inprogress_tasks = Task.objects.filter(status='In Progress').count()
    
    context = {
        'user': request.user,
        'workspace': request.user.department.department_name if request.user.department else 'No Workspace',
        'workspace_code': request.user.department.workspace_code if request.user.department else 'N/A',
        
        # System statistics
        'total_departments': total_departments,
        'total_users': total_users,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        
        # Recent activity
        'recent_projects': recent_projects,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'dashboards/admin_dashboard.html', context)

@login_required
def department_dashboard(request):
    user = request.user
    department = user.department
    
    # Department statistics
    dept_projects = Project.objects.filter(department=department).select_related('project_lead')
    dept_members = User.objects.filter(department=department)
    dept_tasks = Task.objects.filter(project__department=department)
    
    # Task statistics for department
    total_dept_tasks = dept_tasks.count()
    completed_dept_tasks = dept_tasks.filter(status='Completed').count()
    pending_dept_tasks = dept_tasks.filter(status='Pending').count()
    inprogress_dept_tasks = dept_tasks.filter(status='In Progress').count()
    
    # Recent department projects
    recent_dept_projects = dept_projects.order_by('-created_at')[:8]
    
    # Calculate project progress
    projects_with_progress = []
    for project in recent_dept_projects:
        project_tasks = project.tasks.all()
        total_project_tasks = project_tasks.count()
        completed_project_tasks = project_tasks.filter(status='Completed').count()
        progress_percentage = (completed_project_tasks / total_project_tasks * 100) if total_project_tasks > 0 else 0
        
        projects_with_progress.append({
            'project': project,
            'total_tasks': total_project_tasks,
            'completed_tasks': completed_project_tasks,
            'progress_percentage': round(progress_percentage, 1)
        })
    
    context = {
        'user': request.user,
        'workspace': department.department_name if department else 'No Workspace',
        'workspace_code': department.workspace_code if department else 'N/A',
        
        # Department statistics
        'dept_projects_count': dept_projects.count(),
        'dept_members_count': dept_members.count(),
        'total_dept_tasks': total_dept_tasks,
        'completed_dept_tasks': completed_dept_tasks,
        'pending_dept_tasks': pending_dept_tasks,
        'inprogress_dept_tasks': inprogress_dept_tasks,
        
        # Department data
        'dept_projects': projects_with_progress,
        'dept_members': dept_members[:10],
    }
    return render(request, 'dashboards/department_dashboard.html', context)

@login_required
def project_dashboard(request):
    user = request.user
    
    # Projects led by this user
    led_projects = Project.objects.filter(project_lead=user).select_related('department')
    
    # Tasks from led projects
    led_project_tasks = Task.objects.filter(project__project_lead=user).select_related('project', 'assigned_to')
    
    # Task statistics
    total_tasks = led_project_tasks.count()
    completed_tasks = led_project_tasks.filter(status='Completed').count()
    pending_tasks = led_project_tasks.filter(status='Pending').count()
    inprogress_tasks = led_project_tasks.filter(status='In Progress').count()
    
    # Recent tasks from led projects
    recent_tasks = led_project_tasks.order_by('-created_at')[:10]
    
    # Calculate project progress
    projects_with_progress = []
    for project in led_projects:
        project_tasks = project.tasks.all()
        total_project_tasks = project_tasks.count()
        completed_project_tasks = project_tasks.filter(status='Completed').count()
        progress_percentage = (completed_project_tasks / total_project_tasks * 100) if total_project_tasks > 0 else 0
        
        projects_with_progress.append({
            'project': project,
            'total_tasks': total_project_tasks,
            'completed_tasks': completed_project_tasks,
            'progress_percentage': round(progress_percentage, 1)
        })
    
    context = {
        'user': request.user,
        'workspace': user.department.department_name if user.department else 'No Workspace',
        'workspace_code': user.department.workspace_code if user.department else 'N/A',
        
        # Project lead statistics
        'led_projects_count': led_projects.count(),
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'inprogress_tasks': inprogress_tasks,
        
        # Projects and tasks
        'led_projects': projects_with_progress,
        'recent_tasks': recent_tasks,
    }
    return render(request, 'dashboards/project_dashboard.html', context)
