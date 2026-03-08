from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Department

@login_required
def departments_list(request):
    """Display all departments"""
    departments = Department.objects.all().order_by('department_name')
    
    # Add counts for each department
    for dept in departments:
        dept.users_count = dept.users.count()
        dept.projects_count = dept.projects.count()
    
    context = {
        'departments': departments,
    }
    return render(request, 'departments/list.html', context)

@login_required
def department_detail(request, department_id):
    """Display department details and its projects"""
    department = get_object_or_404(Department, id=department_id)
    projects = department.projects.all().order_by('-created_at')
    
    context = {
        'department': department,
        'projects': projects,
        'users_count': department.users.count(),
    }
    return render(request, 'departments/detail.html', context)
