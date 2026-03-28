from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Department

@login_required
def departments_list(request):
    """
    Display departments based on user role
    - Admin and Dept Head: can see all departments
    - Others (project_lead, collaboration): no access
    """
    user = request.user
    if user.role not in ('admin', 'dept_head'):
        return redirect('dashboard')
    departments = Department.objects.all().order_by('department_name')
    
    # Add counts for each department
    for dept in departments:
        dept.users_count = dept.users.count()
        dept.projects_count = dept.projects.count()
        
        # Mark if user can see detailed info
        if user.role == 'admin':
            dept.can_view_details = True
        elif user.role == 'dept_head' and user.department == dept:
            dept.can_view_details = True
        else:
            dept.can_view_details = False
    
    context = {
        'departments': departments,
    }
    return render(request, 'departments/list.html', context)

@login_required
def department_detail(request, department_id):
    """
    Display department details
    - Admin: full access to all departments
    - Dept Head: full access to own department, basic info for others
    - Others: basic info only
    """
    department = get_object_or_404(Department, id=department_id)
    user = request.user
    
    # Determine access level
    full_access = False
    if user.role == 'admin':
        full_access = True
    elif user.role == 'dept_head' and user.department == department:
        full_access = True
    
    if full_access:
        # Show full details including projects
        projects = department.projects.all().order_by('-created_at')
    else:
        # Show basic info only, no projects
        projects = []
    
    context = {
        'department': department,
        'projects': projects,
        'users_count': department.users.count(),
        'full_access': full_access,
    }
    return render(request, 'departments/detail.html', context)
