"""
Test script to verify admin panel functionality
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nexosphere.settings')
django.setup()

from django.contrib.admin.sites import site
from accounts.models import User
from departments.models import Department
from projects.models import Project
from tasks.models import Task
from chat.models import Message

def test_admin_registration():
    """Test that all models are registered in admin"""
    print("Testing Admin Registration...")
    print("=" * 60)
    
    models_to_check = [
        (User, 'accounts', 'User'),
        (Department, 'departments', 'Department'),
        (Project, 'projects', 'Project'),
        (Task, 'tasks', 'Task'),
        (Message, 'chat', 'Message'),
    ]
    
    all_passed = True
    
    for model, app_name, model_name in models_to_check:
        if model in site._registry:
            admin_class = site._registry[model]
            print(f"✓ {app_name}.{model_name} is registered")
            print(f"  Admin class: {admin_class.__class__.__name__}")
            
            # Check for list_display
            if hasattr(admin_class, 'list_display'):
                print(f"  List display: {admin_class.list_display}")
            
            # Check for list_filter
            if hasattr(admin_class, 'list_filter'):
                print(f"  List filters: {admin_class.list_filter}")
            
            # Check for search_fields
            if hasattr(admin_class, 'search_fields'):
                print(f"  Search fields: {admin_class.search_fields}")
            
            print()
        else:
            print(f"✗ {app_name}.{model_name} is NOT registered")
            all_passed = False
            print()
    
    return all_passed

def test_data_integrity():
    """Test that data can be queried correctly"""
    print("\nTesting Data Integrity...")
    print("=" * 60)
    
    tests = [
        ("Users", User.objects.all()),
        ("Departments", Department.objects.all()),
        ("Projects", Project.objects.all()),
        ("Tasks", Task.objects.all()),
        ("Messages", Message.objects.all()),
    ]
    
    all_passed = True
    
    for name, queryset in tests:
        try:
            count = queryset.count()
            print(f"✓ {name}: {count} records")
            
            if count > 0:
                first = queryset.first()
                print(f"  Sample: {first}")
        except Exception as e:
            print(f"✗ {name}: Error - {e}")
            all_passed = False
        print()
    
    return all_passed

def test_relationships():
    """Test that model relationships work correctly"""
    print("\nTesting Model Relationships...")
    print("=" * 60)
    
    all_passed = True
    
    try:
        # Test User -> Department
        users_with_dept = User.objects.filter(department__isnull=False).count()
        print(f"✓ Users with departments: {users_with_dept}")
        
        # Test Department -> Users
        dept = Department.objects.first()
        if dept:
            users_in_dept = dept.users.count()
            print(f"✓ Users in '{dept.department_name}': {users_in_dept}")
        
        # Test Project -> Members (ManyToMany)
        project = Project.objects.first()
        if project:
            members = project.members.count()
            print(f"✓ Members in '{project.project_name}': {members}")
        
        # Test Task -> Project
        tasks_with_project = Task.objects.filter(project__isnull=False).count()
        print(f"✓ Tasks with projects: {tasks_with_project}")
        
        # Test Message -> Project
        messages_with_project = Message.objects.filter(project__isnull=False).count()
        print(f"✓ Messages with projects: {messages_with_project}")
        
        print("\n✓ All relationship tests passed!")
        
    except Exception as e:
        print(f"\n✗ Relationship test failed: {e}")
        all_passed = False
    
    return all_passed

def test_admin_methods():
    """Test custom admin methods"""
    print("\nTesting Custom Admin Methods...")
    print("=" * 60)
    
    all_passed = True
    
    try:
        # Test Message admin's message_preview method
        from chat.admin import MessageAdmin
        message = Message.objects.first()
        if message:
            admin = MessageAdmin(Message, site)
            preview = admin.message_preview(message)
            print(f"✓ MessageAdmin.message_preview() works")
            print(f"  Preview: {preview}")
        
        print("\n✓ All custom method tests passed!")
        
    except Exception as e:
        print(f"\n✗ Custom method test failed: {e}")
        all_passed = False
    
    return all_passed

def main():
    print("\n" + "=" * 60)
    print("NEXUSPHERE ADMIN PANEL TEST SUITE")
    print("=" * 60 + "\n")
    
    results = []
    
    # Run all tests
    results.append(("Admin Registration", test_admin_registration()))
    results.append(("Data Integrity", test_data_integrity()))
    results.append(("Model Relationships", test_relationships()))
    results.append(("Custom Admin Methods", test_admin_methods()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
    else:
        print("✗ SOME TESTS FAILED")
    print("=" * 60 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
