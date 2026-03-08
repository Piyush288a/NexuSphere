import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexusphere.settings')
django.setup()

from departments.models import Department
from accounts.models import User
from projects.models import Project
from tasks.models import Task
from chat.models import Message

print("="*70)
print("CREATING COMPREHENSIVE TEST DATA FOR NEXUSPHERE")
print("="*70)
print()

# Clear existing data (optional - comment out if you want to keep existing data)
print("Clearing existing test data...")
Task.objects.all().delete()
Message.objects.all().delete()
Project.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
Department.objects.all().delete()
print("✓ Cleared existing data\n")

# ============================================================================
# STEP 1: CREATE DEPARTMENTS
# ============================================================================
print("STEP 1: Creating Departments")
print("-" * 70)

cs_dept = Department.objects.create(
    department_name='Computer Science',
    workspace_code='CS'
)
print(f"✓ Created: {cs_dept.department_name} (Workspace: {cs_dept.workspace_code})")

mech_dept = Department.objects.create(
    department_name='Mechanical',
    workspace_code='MECH'
)
print(f"✓ Created: {mech_dept.department_name} (Workspace: {mech_dept.workspace_code})")
print()

# ============================================================================
# STEP 2: CREATE USERS
# ============================================================================
print("STEP 2: Creating Users")
print("-" * 70)

# Admin User
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@nexusphere.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'admin',
        'department': cs_dept,
        'is_staff': True,
        'is_superuser': True
    }
)
if created:
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"✓ Created Admin: {admin_user.username} (Role: {admin_user.role}, Dept: {admin_user.department.workspace_code})")
else:
    admin_user.department = cs_dept
    admin_user.role = 'admin'
    admin_user.set_password('admin123')
    admin_user.save()
    print(f"✓ Updated Admin: {admin_user.username} (Role: {admin_user.role}, Dept: {admin_user.department.workspace_code})")

# Department Head
dept_head_cs = User.objects.create_user(
    username='dept_head_cs',
    email='depthead@nexusphere.com',
    password='dept123',
    first_name='John',
    last_name='Smith',
    role='dept_head',
    department=cs_dept
)
print(f"✓ Created Dept Head: {dept_head_cs.username} (Role: {dept_head_cs.role}, Dept: {dept_head_cs.department.workspace_code})")

# Project Lead
lead_cs = User.objects.create_user(
    username='lead_cs',
    email='lead@nexusphere.com',
    password='lead123',
    first_name='Sarah',
    last_name='Johnson',
    role='project_lead',
    department=cs_dept
)
print(f"✓ Created Project Lead: {lead_cs.username} (Role: {lead_cs.role}, Dept: {lead_cs.department.workspace_code})")

# Member
member_cs = User.objects.create_user(
    username='member_cs',
    email='member@nexusphere.com',
    password='member123',
    first_name='Mike',
    last_name='Davis',
    role='member',
    department=cs_dept
)
print(f"✓ Created Member: {member_cs.username} (Role: {member_cs.role}, Dept: {member_cs.department.workspace_code})")

# Additional member for MECH department
member_mech = User.objects.create_user(
    username='member_mech',
    email='member_mech@nexusphere.com',
    password='member123',
    first_name='Alex',
    last_name='Brown',
    role='member',
    department=mech_dept
)
print(f"✓ Created Member: {member_mech.username} (Role: {member_mech.role}, Dept: {member_mech.department.workspace_code})")
print()

# Update department heads
cs_dept.department_head = dept_head_cs
cs_dept.save()
print(f"✓ Assigned {dept_head_cs.username} as head of {cs_dept.department_name}")
print()

# ============================================================================
# STEP 3: CREATE PROJECTS
# ============================================================================
print("STEP 3: Creating Projects")
print("-" * 70)

project1 = Project.objects.create(
    project_name='AI Attendance System',
    description='Develop an AI-powered attendance tracking system using facial recognition',
    department=cs_dept,
    project_lead=lead_cs,
    deadline=date.today() + timedelta(days=90)
)
project1.members.add(member_cs, lead_cs)
print(f"✓ Created Project: {project1.project_name}")
print(f"  - Department: {project1.department.department_name}")
print(f"  - Lead: {project1.project_lead.username}")
print(f"  - Members: {', '.join([m.username for m in project1.members.all()])}")
print(f"  - Deadline: {project1.deadline}")

project2 = Project.objects.create(
    project_name='Student Portal Redesign',
    description='Modernize the student portal with improved UI/UX',
    department=cs_dept,
    project_lead=lead_cs,
    deadline=date.today() + timedelta(days=60)
)
project2.members.add(member_cs)
print(f"✓ Created Project: {project2.project_name}")
print(f"  - Department: {project2.department.department_name}")
print(f"  - Lead: {project2.project_lead.username}")
print(f"  - Members: {', '.join([m.username for m in project2.members.all()])}")
print(f"  - Deadline: {project2.deadline}")
print()

# ============================================================================
# STEP 4: CREATE TASKS
# ============================================================================
print("STEP 4: Creating Tasks")
print("-" * 70)

task1 = Task.objects.create(
    title='Build Login UI',
    description='Design and implement the login interface with workspace authentication',
    project=project1,
    assigned_to=member_cs,
    deadline=date.today() + timedelta(days=14),
    status='Pending',
    priority='Medium'
)
print(f"✓ Created Task: {task1.title}")
print(f"  - Project: {task1.project.project_name}")
print(f"  - Assigned to: {task1.assigned_to.username}")
print(f"  - Status: {task1.status}, Priority: {task1.priority}")

task2 = Task.objects.create(
    title='Setup Database Schema',
    description='Design and implement the database models for attendance tracking',
    project=project1,
    assigned_to=lead_cs,
    deadline=date.today() + timedelta(days=7),
    status='In Progress',
    priority='High'
)
print(f"✓ Created Task: {task2.title}")
print(f"  - Project: {task2.project.project_name}")
print(f"  - Assigned to: {task2.assigned_to.username}")
print(f"  - Status: {task2.status}, Priority: {task2.priority}")

task3 = Task.objects.create(
    title='Implement Facial Recognition',
    description='Integrate facial recognition API for attendance marking',
    project=project1,
    assigned_to=member_cs,
    deadline=date.today() + timedelta(days=30),
    status='Pending',
    priority='High'
)
print(f"✓ Created Task: {task3.title}")
print(f"  - Project: {task3.project.project_name}")
print(f"  - Assigned to: {task3.assigned_to.username}")
print(f"  - Status: {task3.status}, Priority: {task3.priority}")

task4 = Task.objects.create(
    title='Design Dashboard Mockups',
    description='Create UI mockups for the student portal dashboard',
    project=project2,
    assigned_to=member_cs,
    deadline=date.today() + timedelta(days=10),
    status='Completed',
    priority='Medium'
)
print(f"✓ Created Task: {task4.title}")
print(f"  - Project: {task4.project.project_name}")
print(f"  - Assigned to: {task4.assigned_to.username}")
print(f"  - Status: {task4.status}, Priority: {task4.priority}")
print()

# ============================================================================
# STEP 5: CREATE MESSAGES
# ============================================================================
print("STEP 5: Creating Messages")
print("-" * 70)

message1 = Message.objects.create(
    project=project1,
    sender=lead_cs,
    message_text='Welcome to the AI Attendance System project! Let\'s start with the database design.'
)
print(f"✓ Created Message in {message1.project.project_name} by {message1.sender.username}")

message2 = Message.objects.create(
    project=project1,
    sender=member_cs,
    message_text='I\'ve started working on the login UI. Should be ready for review by end of week.'
)
print(f"✓ Created Message in {message2.project.project_name} by {message2.sender.username}")

message3 = Message.objects.create(
    project=project2,
    sender=lead_cs,
    message_text='Great work on the dashboard mockups! They look fantastic.'
)
print(f"✓ Created Message in {message3.project.project_name} by {message3.sender.username}")
print()

# ============================================================================
# SUMMARY
# ============================================================================
print("="*70)
print("TEST DATA CREATION COMPLETE!")
print("="*70)
print()
print("DATABASE SUMMARY:")
print("-" * 70)
print(f"Departments: {Department.objects.count()}")
print(f"Users: {User.objects.count()}")
print(f"Projects: {Project.objects.count()}")
print(f"Tasks: {Task.objects.count()}")
print(f"Messages: {Message.objects.count()}")
print()

print("="*70)
print("TEST CREDENTIALS")
print("="*70)
print()

credentials = [
    {
        'role': 'Admin',
        'workspace': 'CS',
        'username': 'admin',
        'password': 'admin123',
        'redirect': '/admin-dashboard/'
    },
    {
        'role': 'Department Head',
        'workspace': 'CS',
        'username': 'dept_head_cs',
        'password': 'dept123',
        'redirect': '/department-dashboard/'
    },
    {
        'role': 'Project Lead',
        'workspace': 'CS',
        'username': 'lead_cs',
        'password': 'lead123',
        'redirect': '/project-dashboard/'
    },
    {
        'role': 'Member (CS)',
        'workspace': 'CS',
        'username': 'member_cs',
        'password': 'member123',
        'redirect': '/dashboard/'
    },
    {
        'role': 'Member (MECH)',
        'workspace': 'MECH',
        'username': 'member_mech',
        'password': 'member123',
        'redirect': '/dashboard/'
    }
]

for cred in credentials:
    print(f"{cred['role']}:")
    print(f"  Workspace Code: {cred['workspace']}")
    print(f"  Username: {cred['username']}")
    print(f"  Password: {cred['password']}")
    print(f"  Expected Redirect: {cred['redirect']}")
    print()

print("="*70)
print("WORKSPACE VALIDATION TEST CASES")
print("="*70)
print()
print("✓ Valid Login: workspace=CS, username=admin, password=admin123")
print("✗ Invalid Workspace: workspace=INVALID, username=admin, password=admin123")
print("  Expected: 'Workspace not found.'")
print()
print("✗ Invalid Credentials: workspace=CS, username=admin, password=wrong")
print("  Expected: 'Invalid username or password.'")
print()
print("✗ Wrong Workspace: workspace=MECH, username=admin, password=admin123")
print("  Expected: 'Invalid workspace for this user.'")
print()

print("="*70)
print("NEXT STEPS")
print("="*70)
print()
print("1. Start the server: python manage.py runserver")
print("2. Visit: http://127.0.0.1:8000/login/")
print("3. Test login with different roles")
print("4. Verify role-based redirects")
print("5. Check admin panel: http://127.0.0.1:8000/admin/")
print()
print("="*70)
