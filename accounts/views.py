from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from departments.models import Department
from projects.models import Project
from tasks.models import Task
from chat.models import Message
from accounts.models import User

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

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
