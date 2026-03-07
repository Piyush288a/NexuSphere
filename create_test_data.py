"""
Script to create test data for NexuSphere admin panel testing
"""
import os
import django
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexosphere.settings')
django.setup()

from accounts.models import User
from departments.models import Department
from projects.models import Project
from tasks.models import Task
from chat.models import Message

def create_test_data():
    print("Creating test data...")
    
    # Create Departments
    print("\n1. Creating Departments...")
    dept_it = Department.objects.create(
        department_name="IT Department"
    )
    dept_hr = Department.objects.create(
        department_name="HR Department"
    )
    dept_sales = Department.objects.create(
        department_name="Sales Department"
    )
    print(f"   ✓ Created {Department.objects.count()} departments")
    
    # Create Users
    print("\n2. Creating Users...")
    dept_head_it = User.objects.create_user(
        username="john_doe",
        email="john@nexusphere.com",
        password="password123",
        role="dept_head",
        department=dept_it
    )
    
    project_lead = User.objects.create_user(
        username="jane_smith",
        email="jane@nexusphere.com",
        password="password123",
        role="project_lead",
        department=dept_it
    )
    
    member1 = User.objects.create_user(
        username="bob_wilson",
        email="bob@nexusphere.com",
        password="password123",
        role="member",
        department=dept_it
    )
    
    member2 = User.objects.create_user(
        username="alice_brown",
        email="alice@nexusphere.com",
        password="password123",
        role="member",
        department=dept_it
    )
    print(f"   ✓ Created {User.objects.count()} users (including superuser)")
    
    # Update department heads
    dept_it.department_head = dept_head_it
    dept_it.save()
    
    # Create Projects
    print("\n3. Creating Projects...")
    project1 = Project.objects.create(
        project_name="Website Redesign",
        description="Complete redesign of company website",
        department=dept_it,
        project_lead=project_lead,
        deadline=date.today() + timedelta(days=60)
    )
    project1.members.add(project_lead, member1, member2)
    
    project2 = Project.objects.create(
        project_name="Mobile App Development",
        description="Develop mobile app for iOS and Android",
        department=dept_it,
        project_lead=project_lead,
        deadline=date.today() + timedelta(days=90)
    )
    project2.members.add(project_lead, member1)
    print(f"   ✓ Created {Project.objects.count()} projects")
    
    # Create Tasks
    print("\n4. Creating Tasks...")
    task1 = Task.objects.create(
        title="Design Homepage Mockup",
        description="Create mockup for new homepage design",
        project=project1,
        assigned_to=member1,
        deadline=date.today() + timedelta(days=14),
        status="In Progress",
        priority="High"
    )
    
    task2 = Task.objects.create(
        title="Setup Development Environment",
        description="Configure dev environment for the project",
        project=project1,
        assigned_to=member2,
        deadline=date.today() + timedelta(days=7),
        status="Completed",
        priority="Medium"
    )
    
    task3 = Task.objects.create(
        title="Database Schema Design",
        description="Design database schema for mobile app",
        project=project2,
        assigned_to=member1,
        deadline=date.today() + timedelta(days=21),
        status="Pending",
        priority="High"
    )
    print(f"   ✓ Created {Task.objects.count()} tasks")
    
    # Create Messages
    print("\n5. Creating Messages...")
    msg1 = Message.objects.create(
        project=project1,
        sender=project_lead,
        message_text="Team, let's have a kickoff meeting tomorrow at 10 AM."
    )
    
    msg2 = Message.objects.create(
        project=project1,
        sender=member1,
        message_text="Sounds good! I'll prepare the design concepts."
    )
    
    msg3 = Message.objects.create(
        project=project2,
        sender=project_lead,
        message_text="Please review the requirements document I shared."
    )
    print(f"   ✓ Created {Message.objects.count()} messages")
    
    print("\n" + "="*50)
    print("✓ Test data created successfully!")
    print("="*50)
    print("\nSummary:")
    print(f"  • Departments: {Department.objects.count()}")
    print(f"  • Users: {User.objects.count()}")
    print(f"  • Projects: {Project.objects.count()}")
    print(f"  • Tasks: {Task.objects.count()}")
    print(f"  • Messages: {Message.objects.count()}")
    print("\nYou can now log in to the admin panel at:")
    print("  http://127.0.0.1:8000/admin/")
    print("\nSuperuser credentials:")
    print("  Username: admin")
    print("  Password: admin123")

if __name__ == "__main__":
    create_test_data()
