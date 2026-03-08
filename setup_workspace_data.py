import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexusphere.settings')
django.setup()

from departments.models import Department
from accounts.models import User

# Update existing departments with workspace codes
departments_data = [
    {'name': 'IT Department', 'code': 'CS'},
    {'name': 'HR Department', 'code': 'HR'},
    {'name': 'Sales Department', 'code': 'SALES'},
]

print("Setting up workspace codes...")

for dept_data in departments_data:
    try:
        dept = Department.objects.filter(department_name=dept_data['name']).first()
        if dept:
            dept.workspace_code = dept_data['code']
            dept.save()
            print(f"✓ Updated {dept.department_name} with workspace code: {dept.workspace_code}")
        else:
            # Create new department
            dept = Department.objects.create(
                department_name=dept_data['name'],
                workspace_code=dept_data['code']
            )
            print(f"✓ Created {dept.department_name} with workspace code: {dept.workspace_code}")
    except Exception as e:
        print(f"✗ Error with {dept_data['name']}: {e}")

# Ensure admin user exists with CS workspace
try:
    cs_dept = Department.objects.get(workspace_code='CS')
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@nexusphere.com',
            'role': 'admin',
            'department': cs_dept,
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"✓ Created admin user with workspace CS")
    else:
        admin_user.department = cs_dept
        admin_user.role = 'admin'
        admin_user.save()
        print(f"✓ Updated admin user with workspace CS")
except Exception as e:
    print(f"✗ Error creating admin user: {e}")

print("\n" + "="*50)
print("Setup complete!")
print("="*50)
print("\nTest Credentials:")
print("Workspace: CS")
print("Username: admin")
print("Password: admin123")
print("="*50)
