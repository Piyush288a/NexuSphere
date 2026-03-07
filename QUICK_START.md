# NexuSphere - Quick Start Guide

## 🚀 Start the Server

```bash
cd NexuSphere
python manage.py runserver
```

## 🔐 Admin Login

**URL:** http://127.0.0.1:8000/admin/

**Credentials:**
- Username: `admin`
- Password: `admin123`

## 📊 Available Models in Admin

1. **Users** - Manage system users with roles
2. **Departments** - Manage departments and heads
3. **Projects** - Manage projects with members
4. **Tasks** - Manage tasks with status tracking
5. **Messages** - View project chat messages

## 🧪 Test Data

Sample data already created:
- 3 Departments
- 5 Users (including superuser)
- 2 Projects
- 3 Tasks
- 3 Messages

## 🛠️ Useful Commands

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Check for issues
python manage.py check

# Run test suite
python test_admin.py

# Create test data
python create_test_data.py
```

## ✅ System Status

- ✓ All migrations applied
- ✓ Admin panel configured
- ✓ Test data loaded
- ✓ No errors or warnings
- ✓ Ready for Phase 4
