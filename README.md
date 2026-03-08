# NexuSphere - Collaboration Platform

A Django-based collaboration platform for managing departments, projects, tasks, and team communication.

## 📋 Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Features Implemented](#features-implemented)
- [Database Models](#database-models)
- [Installation & Setup](#installation--setup)
- [Usage Guide](#usage-guide)
- [Phase Completion Status](#phase-completion-status)

---

## 🎯 Overview

NexuSphere is a simplified collaboration platform prototype designed to help organizations and college departments manage their workflow efficiently. The platform enables:

- Department management and organization
- Project planning and tracking
- Task assignment and monitoring
- Team communication through project-based messaging
- User role management and access control

---

## 🛠 Technology Stack

- **Backend Framework:** Django 6.0.1
- **Database:** SQLite3 (development)
- **Frontend:** HTML, CSS, Bootstrap 5.3.0
- **Python Version:** 3.13.0
- **Authentication:** Django built-in authentication system

---

## 📁 Project Structure

```
nexusphere/
├── manage.py
├── db.sqlite3
├── README.md
├── .gitignore
│
├── nexusphere/              # Main project configuration
│   ├── settings.py          # Project settings
│   ├── urls.py              # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                # User management app
│   ├── models.py            # Custom User model
│   ├── views.py             # Authentication views
│   ├── urls.py              # Account URLs
│   └── admin.py             # User admin configuration
│
├── departments/             # Department management app
│   ├── models.py            # Department model
│   └── admin.py             # Department admin
│
├── projects/                # Project management app
│   ├── models.py            # Project model
│   └── admin.py             # Project admin
│
├── tasks/                   # Task management app
│   ├── models.py            # Task model
│   └── admin.py             # Task admin
│
├── chat/                    # Messaging app
│   ├── models.py            # Message model
│   └── admin.py             # Message admin
│
└── templates/               # HTML templates
    ├── dashboard.html       # Main dashboard
    ├── base.html            # Base template
    └── registration/
        ├── login.html       # Login page
        └── logged_out.html  # Logout confirmation
```

---

## ✨ Features Implemented

### Phase 1: Project Setup ✅

**Objective:** Initialize Django project and create app structure

**Completed:**
- Django project `nexusphere` created
- Five Django apps created:
  - `accounts` - User management
  - `departments` - Department management
  - `projects` - Project management
  - `tasks` - Task management
  - `chat` - Messaging system
- All apps registered in `INSTALLED_APPS`
- Custom User model configured
- SQLite database setup
- Initial migrations applied
- Development server running successfully

---

### Phase 2: Database Models ✅

**Objective:** Define database schema and relationships

**Models Created:**

#### 1. User Model (accounts/models.py)
- Extends Django's `AbstractUser`
- **Fields:**
  - All default Django User fields (username, email, password, etc.)
  - `role` - CharField with choices (admin, dept_head, project_lead, member)
  - `department` - ForeignKey to Department
- **Purpose:** Custom user model with role-based access and department assignment

#### 2. Department Model (departments/models.py)
- **Fields:**
  - `department_name` - CharField (max 200)
  - `department_head` - ForeignKey to User
  - `created_at` - DateTimeField (auto)
- **Relationships:**
  - One-to-many with Users
  - One-to-many with Projects
- **Purpose:** Organize users and projects into departments

#### 3. Project Model (projects/models.py)
- **Fields:**
  - `project_name` - CharField (max 200)
  - `description` - TextField
  - `department` - ForeignKey to Department
  - `project_lead` - ForeignKey to User
  - `members` - ManyToManyField to User
  - `deadline` - DateField
  - `created_at` - DateTimeField (auto)
- **Relationships:**
  - Belongs to one Department
  - Has one Project Lead (User)
  - Has many Members (Users)
  - Has many Tasks
  - Has many Messages
- **Purpose:** Manage project information and team assignments

#### 4. Task Model (tasks/models.py)
- **Fields:**
  - `title` - CharField (max 200)
  - `description` - TextField
  - `project` - ForeignKey to Project
  - `assigned_to` - ForeignKey to User
  - `deadline` - DateField
  - `status` - CharField with choices (Pending, In Progress, Completed)
  - `priority` - CharField with choices (Low, Medium, High)
  - `created_at` - DateTimeField (auto)
- **Relationships:**
  - Belongs to one Project
  - Assigned to one User
- **Purpose:** Track individual tasks within projects

#### 5. Message Model (chat/models.py)
- **Fields:**
  - `project` - ForeignKey to Project
  - `sender` - ForeignKey to User
  - `message_text` - TextField
  - `file_attachment` - FileField (optional)
  - `created_at` - DateTimeField (auto)
- **Relationships:**
  - Belongs to one Project
  - Sent by one User
- **Purpose:** Enable project-based team communication

**Database Relationships:**
```
Department
├── Users (one-to-many)
├── Projects (one-to-many)
└── Department Head (one-to-one with User)

Project
├── Department (many-to-one)
├── Project Lead (many-to-one with User)
├── Members (many-to-many with User)
├── Tasks (one-to-many)
└── Messages (one-to-many)

User
├── Department (many-to-one)
├── Assigned Tasks (one-to-many)
├── Leading Projects (one-to-many)
└── Sent Messages (one-to-many)
```

---

### Phase 3: Admin Panel Setup ✅

**Objective:** Configure Django Admin for data management

**Admin Configurations:**

#### User Admin (accounts/admin.py)
- Custom UserAdmin extending Django's BaseUserAdmin
- **List Display:** username, email, role, department, is_staff, is_active
- **Filters:** role, department, is_staff, is_active
- **Search:** username, email
- **Fieldsets:** Custom fields for role and department

#### Department Admin (departments/admin.py)
- **List Display:** department_name, department_head, created_at
- **Search:** department_name
- **Filter:** created_at

#### Project Admin (projects/admin.py)
- **List Display:** project_name, department, project_lead, deadline, created_at
- **Filters:** department, deadline, created_at
- **Search:** project_name, description
- **Special Features:**
  - Horizontal filter for members (ManyToMany)
  - Date hierarchy by deadline

#### Task Admin (tasks/admin.py)
- **List Display:** title, project, assigned_to, status, priority, deadline, created_at
- **Filters:** status, priority, deadline, created_at
- **Search:** title, description
- **Special Features:**
  - Date hierarchy by deadline
  - Inline editing for status and priority

#### Message Admin (chat/admin.py)
- **List Display:** project, sender, message_preview, created_at
- **Filters:** project, created_at
- **Search:** message_text
- **Special Features:**
  - Date hierarchy by created_at
  - Custom message_preview method (truncates long messages)
  - Read-only created_at field

**Admin Panel Features:**
- Full CRUD operations for all models
- Advanced filtering and search
- Relationship management
- Data validation
- User-friendly interface

**Test Data:**
- 3 Departments (IT, HR, Sales)
- 5 Users with different roles
- 2 Projects with team members
- 3 Tasks with various statuses
- 3 Messages in projects

---

### Phase 4: Authentication & Dashboard ✅

**Objective:** Implement user authentication and main dashboard

**Authentication System:**

#### Login System
- **URL:** `/login/`
- **Template:** `templates/registration/login.html`
- **Features:**
  - Bootstrap 5 styled form
  - Username and password fields
  - Error message display
  - CSRF protection
  - Responsive design

#### Logout System
- **URL:** `/logout/`
- **Template:** `templates/registration/logged_out.html`
- **Features:**
  - Automatic logout
  - Redirect to login page
  - Session cleanup

#### URL Configuration
- `/` - Home (redirects to login or dashboard)
- `/login/` - Login page
- `/logout/` - Logout action
- `/dashboard/` - Main dashboard (login required)
- `/admin/` - Django admin panel

#### Settings Configuration
```python
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'
```

**Dashboard Features:**

#### Statistics Cards
- **Departments Count** - Total departments in system
- **Projects Count** - Total active projects
- **Tasks Count** - Total tasks across all projects
- **Messages Count** - Total messages in system

#### User Information
- Welcome message with username
- User role display
- Logout button in navigation

#### My Department Section
- Department name
- Department head information
- Displays "Not assigned" if user has no department

#### My Tasks Section
- Lists up to 5 tasks assigned to current user
- Shows task title
- Status badges (Pending, In Progress, Completed)
- Color-coded status indicators:
  - Pending: Gray
  - In Progress: Cyan
  - Completed: Green

#### Recent Projects Table
- Lists 5 most recent projects
- Displays:
  - Project name
  - Department
  - Project lead
  - Deadline date
- Responsive table design
- Hover effects

**UI/UX Features:**
- Bootstrap 5 responsive design
- Mobile-friendly layout
- Color-coded cards for statistics
- Clean navigation bar
- Professional styling
- Accessible design

---

### Phase 4.5: Workspace-Based Authentication Upgrade ✅

**Objective:** Enhance authentication with workspace-based login system

**Workspace Authentication:**

#### Enhanced Login System
- **Three-Factor Login:**
  - Workspace Code (Department identifier)
  - Username
  - Password
- **Validation Flow:**
  1. Verify workspace exists
  2. Authenticate user credentials
  3. Validate user belongs to workspace
- **Error Messages:**
  - "Workspace not found." - Invalid workspace code
  - "Invalid username or password." - Wrong credentials
  - "Invalid workspace for this user." - User not in workspace

#### Department Model Enhancement
- **New Field:** `workspace_code`
  - CharField (max_length=20)
  - Unique constraint
  - Used for workspace identification
- **Migration:** `0003_department_workspace_code`

#### Role-Based Redirects
After successful login, users are redirected based on their role:
- **admin** → `/admin-dashboard/`
- **dept_head** → `/department-dashboard/`
- **project_lead** → `/project-dashboard/`
- **member** → `/dashboard/`

#### Role-Specific Dashboards
Created dedicated dashboard templates for each role:
- `templates/dashboards/admin_dashboard.html`
- `templates/dashboards/department_dashboard.html`
- `templates/dashboards/project_dashboard.html`
- `templates/dashboard.html` (member dashboard)

**Dashboard Features by Role:**

##### Admin Dashboard
- Full system overview
- User management access
- Department statistics
- System-wide metrics
- Quick links to admin panel

##### Department Head Dashboard
- Department-specific metrics
- Team member overview
- Department projects
- Resource allocation view

##### Project Lead Dashboard
- Led projects overview
- Team member status
- Task progress tracking
- Project deadlines

##### Member Dashboard
- Assigned tasks
- Project participation
- Personal statistics
- Recent activity

**UI Enhancements:**
- Consistent beige/dark grey/white color scheme
- Modern, sleek design
- 3D dynamic effects
- Floating background shapes
- Smooth animations and transitions
- Gradient buttons with shine effects
- Hover effects on interactive elements
- Inter font from Google Fonts

**Color Palette:**
- Background: #F5F1E8 (Beige)
- Cards: #FFFFFF (White)
- Primary Text: #2C2C2C (Dark Grey)
- Secondary Text: #4A4A4A (Medium Grey)
- Borders: #E8E4DC (Light Grey)
- Accent: #8B7355 (Brown)
- Gradients: #8B7355 to #2C2C2C

---

### Phase 5: Views & Templates (Departments & Projects) ✅

**Objective:** Implement full CRUD views and templates for Departments and Projects

**Base Template System:**

#### Base Template (`templates/base.html`)
- **Navigation Bar:**
  - Logo/Brand name
  - Dashboard link
  - Departments link
  - Projects link
  - User info display
  - Logout button
- **Features:**
  - Sticky navigation
  - Active link highlighting
  - Responsive design
  - Consistent across all pages
  - Beige background (#F5F1E8)
  - Inter font family

---

**Departments Module:**

#### Views (`departments/views.py`)

##### departments_list
- **URL:** `/departments/`
- **Access:** All authenticated users
- **Features:**
  - Lists all departments
  - Shows workspace code
  - Displays department head
  - Shows user count
  - Shows project count
  - Grid layout with cards
  - Hover animations

##### department_detail
- **URL:** `/departments/<id>/`
- **Access:** All authenticated users
- **Features:**
  - Department information
  - Workspace code badge
  - Department head details
  - List of all projects in department
  - User statistics
  - Back navigation link
  - Empty state handling

#### Templates

##### departments/list.html
- Grid layout (3 columns on desktop)
- Department cards with:
  - Department name
  - Workspace code badge
  - Department head name
  - User count
  - Project count
- Hover effects (lift and shadow)
- Empty state message
- Consistent beige/white design

##### departments/detail.html
- Department header section
- Workspace code badge
- Department metadata
- Projects grid
- Empty state for no projects
- Back to list link
- Responsive layout

---

**Projects Module:**

#### Views (`projects/views.py`)

##### projects_list
- **URL:** `/projects/`
- **Access:** Role-based
  - **Admin:** See all projects
  - **Dept Head:** See department projects
  - **Project Lead:** See led projects
  - **Member:** See assigned projects
- **Features:**
  - Filtered project list
  - Shows project name
  - Shows department
  - Shows project lead
  - Shows deadline
  - Shows member count
  - Grid layout

##### project_detail
- **URL:** `/projects/<id>/`
- **Access:** Permission-based
  - Admin: Full access
  - Dept Head: Department projects
  - Project Lead: Led projects
  - Members: Assigned projects
- **Features:**
  - Project information
  - Description
  - Team members list
  - Tasks list with status
  - Access control (404 if unauthorized)
  - Empty states

#### Templates

##### projects/list.html
- Grid layout (3 columns)
- Project cards with:
  - Project name
  - Department badge
  - Project lead
  - Deadline
  - Member count
  - Top gradient bar
- Hover effects
- Empty state message
- Role-based content

##### projects/detail.html
- Project header with full details
- Description section
- Team members grid with roles
- Tasks list with:
  - Task title
  - Assigned user
  - Status badge (color-coded)
  - Priority indicator
- Empty states for members/tasks
- Back to list link
- Access-controlled content

---

**UI Design Consistency:**

#### Design Elements
- **Border Radius:** 12px for cards, 8px for badges
- **Padding:** 24-32px for cards
- **Gaps:** 20-24px in grids
- **Transitions:** 0.3s ease for all animations
- **Hover Effects:** translateY(-4px) with shadow
- **Font:** Inter (Google Fonts)

#### Consistent Components
- Card hover effects
- Badge styling (department, status, priority)
- Empty states with icons
- Back navigation links
- Grid layouts (responsive)
- Status badges (color-coded)
- Meta information display

#### Status Badge Colors
- **Pending:** #6C757D (Grey)
- **In Progress:** #0DCAF0 (Cyan)
- **Completed:** #198754 (Green)

#### Priority Badge Colors
- **Low:** #6C757D (Grey)
- **Medium:** #FFC107 (Yellow)
- **High:** #DC3545 (Red)

---

**Access Control Implementation:**

#### Department Access
- All authenticated users can view departments
- All authenticated users can view department details

#### Project Access
- **Admin:** Full access to all projects
- **Dept Head:** Access to department projects only
- **Project Lead:** Access to led projects
- **Members:** Access to assigned projects only
- **Unauthorized:** 404 error page

---

**Data Display:**

#### Departments List
- Department name
- Workspace code
- Department head
- User count
- Project count

#### Department Detail
- Full department information
- All projects in department
- User statistics
- Department head info

#### Projects List
- Project name
- Department name
- Project lead
- Deadline
- Member count

#### Project Detail
- Project name and description
- Department
- Project lead
- Deadline
- Team members (with roles)
- Tasks (with status and assignee)
- Member count
- Task count

---

**Test Data:**

Created comprehensive test data using `create_comprehensive_test_data.py`:
- **2 Departments:** Computer Science (CS), Mechanical (MECH)
- **5 Users:** admin, dept_head_cs, lead_cs, member_cs, member_mech
- **2 Projects:** AI Attendance System, Student Portal Redesign
- **4 Tasks:** Various statuses and priorities
- **3 Messages:** Project communications

All test credentials documented in `TEST_CREDENTIALS.md`

---

## 🗄 Database Models

### Entity Relationship Diagram

```
┌─────────────────┐
│   Department    │
├─────────────────┤
│ id (PK)         │
│ department_name │
│ department_head │◄────┐
│ created_at      │     │
└─────────────────┘     │
        │               │
        │ 1:N           │
        ▼               │
┌─────────────────┐     │
│     Project     │     │
├─────────────────┤     │
│ id (PK)         │     │
│ project_name    │     │
│ description     │     │
│ department_id   │     │
│ project_lead_id │─────┤
│ deadline        │     │
│ created_at      │     │
└─────────────────┘     │
        │               │
        │ 1:N           │
        ├───────────────┤
        │               │
        ▼               │
┌─────────────────┐     │
│      Task       │     │
├─────────────────┤     │
│ id (PK)         │     │
│ title           │     │
│ description     │     │
│ project_id      │     │
│ assigned_to_id  │─────┤
│ deadline        │     │
│ status          │     │
│ priority        │     │
│ created_at      │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │
│     Message     │     │
├─────────────────┤     │
│ id (PK)         │     │
│ project_id      │     │
│ sender_id       │─────┤
│ message_text    │     │
│ file_attachment │     │
│ created_at      │     │
└─────────────────┘     │
                        │
┌─────────────────┐     │
│      User       │     │
├─────────────────┤     │
│ id (PK)         │◄────┘
│ username        │
│ email           │
│ password        │
│ role            │
│ department_id   │
│ first_name      │
│ last_name       │
│ is_staff        │
│ is_active       │
└─────────────────┘
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.13.0 or higher
- pip (Python package manager)
- Git

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Piyush288a/NexuSphere.git
cd NexuSphere
```

2. **Create virtual environment (optional but recommended)**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Django**
```bash
pip install django
```

4. **Navigate to project directory**
```bash
cd nexusphere
```

5. **Run migrations**
```bash
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```
Follow the prompts to create admin credentials.

7. **Load test data**
```bash
python create_comprehensive_test_data.py
```

8. **Start development server**
```bash
python manage.py runserver
```

9. **Access the application**
- Main site: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/
- Login page: http://127.0.0.1:8000/login/
- Dashboard: http://127.0.0.1:8000/dashboard/

---

## 📖 Usage Guide

### For Administrators

1. **Access Admin Panel**
   - Navigate to http://127.0.0.1:8000/admin/
   - Login with superuser credentials

2. **Create Departments**
   - Go to Departments section
   - Click "Add Department"
   - Enter department name and assign department head
   - Save

3. **Create Users**
   - Go to Users section
   - Click "Add User"
   - Fill in username, password, email
   - Assign role (admin, dept_head, project_lead, member)
   - Assign to department
   - Save

4. **Create Projects**
   - Go to Projects section
   - Click "Add Project"
   - Enter project details
   - Select department
   - Assign project lead
   - Add team members
   - Set deadline
   - Save

5. **Create Tasks**
   - Go to Tasks section
   - Click "Add Task"
   - Enter task details
   - Select project
   - Assign to user
   - Set status and priority
   - Set deadline
   - Save

6. **Manage Messages**
   - Go to Messages section
   - View project communications
   - Filter by project or date

### For Regular Users

1. **Login**
   - Navigate to http://127.0.0.1:8000/
   - Enter username and password
   - Click Login

2. **View Dashboard**
   - See system statistics
   - View your department info
   - Check assigned tasks
   - Browse recent projects

3. **Logout**
   - Click Logout button in navigation bar

### Default Credentials

All test users use workspace-based login (workspace_code + username + password):

**Admin User:**
- **Workspace Code:** `CS`
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Admin
- **Department:** Computer Science
- **Redirect:** `/admin-dashboard/`
- **Access:** Full system access, superuser privileges

**Department Head:**
- **Workspace Code:** `CS`
- **Username:** `dept_head`
- **Password:** `dept123`
- **Role:** Department Head
- **Department:** Computer Science
- **Redirect:** `/department-dashboard/`
- **Access:** Department management

**Project Lead:**
- **Workspace Code:** `CS`
- **Username:** `project_lead`
- **Password:** `lead123`
- **Role:** Project Lead
- **Department:** Computer Science
- **Redirect:** `/project-dashboard/`
- **Access:** Project management, leads 2 projects

**Member (Computer Science):**
- **Workspace Code:** `CS`
- **Username:** `member_cs`
- **Password:** `member123`
- **Role:** Member
- **Department:** Computer Science
- **Redirect:** `/dashboard/`
- **Access:** Basic access, assigned to 3 tasks

**Member (Mechanical):**
- **Workspace Code:** `MECH`
- **Username:** `member_mech`
- **Password:** `member123`
- **Role:** Member
- **Department:** Mechanical
- **Redirect:** `/dashboard/`
- **Access:** Basic access

#### Test Login Scenarios

**Valid Login:**
```
Workspace: CS
Username: admin
Password: admin123
Result: Success → Redirect to /admin-dashboard/
```

**Invalid Workspace:**
```
Workspace: INVALID
Username: admin
Password: admin123
Result: Error → "Workspace not found."
```

**Invalid Credentials:**
```
Workspace: CS
Username: admin
Password: wrongpassword
Result: Error → "Invalid username or password."
```

**Wrong Workspace:**
```
Workspace: MECH
Username: admin
Password: admin123
Result: Error → "Invalid workspace for this user."
```

For complete test data details, see `TEST_CREDENTIALS.md`

---

## 📊 Phase Completion Status

| Phase | Title | Status | Description |
|-------|-------|--------|-------------|
| 1 | Project Setup | ✅ Complete | Django project and apps created |
| 2 | Database Models | ✅ Complete | All models and relationships defined |
| 3 | Admin Panel | ✅ Complete | Admin interface configured |
| 4 | Authentication & Dashboard | ✅ Complete | Login system and dashboard implemented |
| 4.5 | Workspace Authentication | ✅ Complete | Workspace-based login and role dashboards |
| 5 | Views & Templates | ✅ Complete | Departments and Projects CRUD views |
| 6 | Task Management | 🔄 Pending | Task CRUD operations and views |
| 7 | REST API | 🔄 Pending | API endpoints for frontend |
| 8 | Frontend Enhancement | 🔄 Pending | Advanced UI features |
| 9 | Real-time Chat | 🔄 Pending | WebSocket implementation |

---

## 🔐 Security Features

- CSRF protection enabled
- Password hashing (Django default)
- Login required decorators
- Session management
- SQL injection protection (Django ORM)
- XSS protection (Django templates)

---

## 🎨 UI Components

### Bootstrap 5 Components Used
- Navigation bar
- Cards
- Tables
- Forms
- Buttons
- Badges
- Alerts
- Grid system
- Responsive utilities

### Color Scheme
- Primary: Blue (#0d6efd)
- Success: Green (#198754)
- Warning: Yellow (#ffc107)
- Info: Cyan (#0dcaf0)
- Danger: Red (#dc3545)

---

## 📝 Database Schema Details

### User Roles
- `admin` - Full system access
- `dept_head` - Department management
- `project_lead` - Project management
- `member` - Basic access

### Task Status Options
- `Pending` - Not started
- `In Progress` - Currently working
- `Completed` - Finished

### Task Priority Levels
- `Low` - Can wait
- `Medium` - Normal priority
- `High` - Urgent

---

## 🔧 Configuration Files

### settings.py Key Settings
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'departments',
    'projects',
    'tasks',
    'chat',
]

AUTH_USER_MODEL = 'accounts.User'

LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_URL = '/login/'

TEMPLATES = [{
    'DIRS': [BASE_DIR / 'templates'],
    ...
}]
```

---

## 🐛 Known Issues

None at this time. All Phase 1-5 features are working as expected.

---

## 🚀 Future Enhancements

- Task management views and forms
- User profile pages
- Project/task creation and editing forms
- Real-time notifications
- File upload for tasks and messages
- Advanced search and filtering
- Activity logs and audit trails
- Email notifications
- Export functionality (PDF, Excel)
- Calendar view for deadlines
- Gantt charts for projects
- Real-time chat with WebSockets
- Mobile app integration
- API documentation
- Performance optimization

---

## 👥 Contributors

- **Piyush288a** - Initial development and Phases 1-3
- **Darshan-Dalsaniya** - Phases 4-5 implementation
- Email: dalsaniyadarshan122@gmail.com
- GitHub: https://github.com/Piyush288a/NexuSphere

---

## 📄 License

This project is developed as a prototype for educational purposes.

---

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Contact: piyush288a@gmail.com

---

## 🙏 Acknowledgments

- Django Documentation
- Bootstrap Documentation
- Python Community

---

**Last Updated:** March 8, 2026  
**Version:** 1.5.0 (Phase 5 Complete)  
**Django Version:** 6.0.1  
**Python Version:** 3.13.0
