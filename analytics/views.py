from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import date
from tasks.models import Task
from projects.models import Project
from departments.models import Department
from accounts.models import User


@login_required
def user_analytics(request):
    """
    User Analytics API
    Returns personal task statistics for the logged-in user
    """
    user = request.user
    
    # Get all tasks assigned to user
    user_tasks = Task.objects.filter(assigned_to=user)
    
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='Completed').count()
    pending_tasks = user_tasks.filter(status='Pending').count()
    in_progress_tasks = user_tasks.filter(status='In Progress').count()
    
    # Overdue tasks: deadline < today AND status != Completed
    today = date.today()
    overdue_tasks = user_tasks.filter(
        deadline__lt=today,
        status__in=['Pending', 'In Progress']
    ).count()
    
    # Completion rate
    completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Efficiency score: on-time completed tasks / total completed tasks
    on_time_completed = user_tasks.filter(
        status='Completed',
        deadline__gte=today
    ).count()
    efficiency_score = (on_time_completed / completed_tasks * 100) if completed_tasks > 0 else 0
    
    data = {
        'user_id': user.id,
        'username': user.username,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'completion_rate': round(completion_rate, 2),
        'efficiency_score': round(efficiency_score, 2),
    }
    
    return JsonResponse(data)


@login_required
def project_analytics(request, project_id):
    """
    Project Analytics API
    Returns statistics for a specific project
    Access: Project members, lead, dept_head, admin
    """
    user = request.user
    
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return JsonResponse({'error': 'Project not found'}, status=404)
    
    # Access control
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
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Get project tasks
    project_tasks = project.tasks.all()
    
    total_tasks = project_tasks.count()
    completed_tasks = project_tasks.filter(status='Completed').count()
    pending_tasks = project_tasks.filter(status='Pending').count()
    in_progress_tasks = project_tasks.filter(status='In Progress').count()
    
    # Completion percentage
    completion_percentage = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Active members (members with assigned tasks)
    active_members = project.members.filter(assigned_tasks__project=project).distinct().count()
    
    # Overdue tasks
    today = date.today()
    overdue_tasks = project_tasks.filter(
        deadline__lt=today,
        status__in=['Pending', 'In Progress']
    ).count()
    
    data = {
        'project_id': project.id,
        'project_name': project.project_name,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completion_percentage': round(completion_percentage, 2),
        'active_members': active_members,
        'total_members': project.members.count(),
        'overdue_tasks': overdue_tasks,
    }
    
    return JsonResponse(data)


@login_required
def department_analytics(request, department_id):
    """
    Department Analytics API
    Returns statistics for a specific department
    Access: Dept_head (own dept), admin
    """
    user = request.user
    
    try:
        department = Department.objects.get(id=department_id)
    except Department.DoesNotExist:
        return JsonResponse({'error': 'Department not found'}, status=404)
    
    # Access control
    has_access = False
    if user.role == 'admin':
        has_access = True
    elif user.role == 'dept_head' and user.department == department:
        has_access = True
    
    if not has_access:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Department projects
    dept_projects = Project.objects.filter(department=department)
    total_projects = dept_projects.count()
    
    # Department tasks
    dept_tasks = Task.objects.filter(project__department=department)
    total_tasks = dept_tasks.count()
    completed_tasks = dept_tasks.filter(status='Completed').count()
    
    # Average completion rate
    avg_completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Productivity score (projects with >50% completion)
    productive_projects = 0
    for project in dept_projects:
        project_tasks = project.tasks.all()
        if project_tasks.count() > 0:
            completion = project_tasks.filter(status='Completed').count() / project_tasks.count()
            if completion > 0.5:
                productive_projects += 1
    
    productivity_score = (productive_projects / total_projects * 100) if total_projects > 0 else 0
    
    data = {
        'department_id': department.id,
        'department_name': department.department_name,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'avg_completion_rate': round(avg_completion_rate, 2),
        'productivity_score': round(productivity_score, 2),
        'total_members': department.users.count(),
    }
    
    return JsonResponse(data)


@login_required
def system_analytics(request):
    """
    System-Wide Analytics API
    Returns global statistics
    Access: Admin only
    """
    user = request.user
    
    # Access control - admin only
    if user.role != 'admin':
        return JsonResponse({'error': 'Access denied. Admin only.'}, status=403)
    
    # System-wide statistics
    total_users = User.objects.count()
    total_departments = Department.objects.count()
    total_projects = Project.objects.count()
    total_tasks = Task.objects.count()
    
    completed_tasks = Task.objects.filter(status='Completed').count()
    
    # System efficiency: overall completion rate
    system_efficiency = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
    
    # Active users (users with assigned tasks)
    active_users = User.objects.filter(assigned_tasks__isnull=False).distinct().count()
    
    data = {
        'total_users': total_users,
        'active_users': active_users,
        'total_departments': total_departments,
        'total_projects': total_projects,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'system_efficiency': round(system_efficiency, 2),
    }
    
    return JsonResponse(data)
