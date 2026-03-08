import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexusphere.settings')
django.setup()

from departments.models import Department
from accounts.models import User
from projects.models import Project
from tasks.models import Task
from chat.models import Message

print("="*70)
print("DATABASE VERIFICATION")
print("="*70)
print()
print(f"Departments: {Department.objects.count()}")
print(f"Users: {User.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"Tasks: {Task.objects.count()}")
print(f"Messages: {Message.objects.count()}")
print()

print("="*70)
print("USERS BY ROLE")
print("="*70)
for role_code, role_name in User.ROLE_CHOICES:
    users = User.objects.filter(role=role_code)
    if users.exists():
        print(f"\n{role_name}:")
        for user in users:
            dept = user.department.workspace_code if user.department else 'None'
            print(f"  - {user.username} (Workspace: {dept})")

print()
print("="*70)
print("PROJECTS")
print("="*70)
for project in Project.objects.all():
    print(f"\n{project.project_name}:")
    print(f"  Department: {project.department.department_name}")
    print(f"  Lead: {project.project_lead.username if project.project_lead else 'None'}")
    print(f"  Members: {', '.join([m.username for m in project.members.all()])}")
    print(f"  Tasks: {project.tasks.count()}")

print()
print("="*70)
print("VERIFICATION COMPLETE")
print("="*70)
