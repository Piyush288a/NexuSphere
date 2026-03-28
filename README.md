# NexuSphere - Collaboration Platform

A Django-based collaboration platform for managing departments, projects, tasks, and team communication with full Role-Based Access Control (RBAC).

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Requirements](#system-requirements)
- [Project Structure](#project-structure)
- [Role System](#role-system)
- [Project Proposal Workflow](#project-proposal-workflow)
- [Analytics System](#analytics-system)
- [Database Models](#database-models)
- [Installation & Setup](#installation--setup)
- [Test Credentials](#test-credentials)
- [URL Endpoints](#url-endpoints)
- [Security Features](#security-features)
- [Future Enhancements](#future-enhancements)
- [Contributors](#contributors)

---

## 🎯 Overview

NexuSphere is a production-level collaboration platform for organizations and college departments to manage workflow efficiently. It features a complete RBAC system, project proposal workflow, analytics APIs, and role-based dashboards.

---

## 🌟 Key Features

### 🔐 Authentication & Security
- Workspace-based login (workspace_code + username + password)
- Role-based access control (Admin, Department Head, Project Lead, Collaboration)
- Session management and secure logout
- Protected routes with authentication requirements

### 🏢 Department Management
- View all departments with workspace codes
- Role-based access: Admin and Dept Head get full details, others get basic info
- Department statistics (users, projects)

### 📁 Project Management
- Project Proposal workflow (Dept Head proposes → Admin approves → Project created)
- Role-based project visibility
- Project details with task tracking and team members
- Access control enforcement

### ✅ Task Management
- Create and assign tasks to team members
- Task status tracking (Pending → In Progress → Completed)
- Priority levels (Low, Medium, High)
- Status update authorization

### 💬 Team Communication
- Project-based chat system
- Text messages with optional file attachments
- Message history with timestamps

### 📊 Analytics System
- REST API endpoints for user, project, department, and system analytics
- Completion rate, efficiency score, overdue tasks, productivity score
- Role-based data access

### 🎨 UI/UX
- Modern dark sidebar with Tailwind CSS
- Inter font, responsive design
- Role-based dynamic navigation
- Progress bars, status badges, empty states

---

## 🛠 Technology Stack

- **Backend:** Django 6.0.1
- **Database:** SQLite3 (development)
- **Frontend:** HTML, Tailwind CSS, Inter font
- **Python:** 3.13.0
- **Authentication:** Django built-in + custom workspace auth

---

## 💻 System Requirements

- Python 3.13.0+
- pip (latest)
- Git
- 2GB RAM minimum
- 500MB free storage

---

## 📁 Project Structure

```
nexusphere/
├── manage.py
├── db.sqlite3
├── nexusphere/              # Main project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                # User management & auth
├── departments/             # Department management
├── projects/                # Projects & proposals
├── tasks/                   # Task management
├── chat/                    # Messaging system
├── analytics/               # Analytics REST APIs
└── templates/               # HTML templates
    ├── base.html
    ├── base_auth.html
    ├── base_navbar.html     # Role-based navigation
    ├── dashboard.html
    ├── dashboards/
    ├── departments/
    ├── projects/            # Includes proposal templates
    ├── tasks/
    ├── chat/
    └── registration/
```

---

## 👥 Role System

NexuSphere uses four roles with distinct permissions:

| Feature | Admin | Dept Head | Project Lead | Collaboration |
|---------|-------|-----------|--------------|---------------|
| View All Departments | ✅ Full | ✅ Basic | ❌ | ❌ |
| View Own Department | ✅ | ✅ Full | ❌ | ❌ |
| View All Projects | ✅ | ✅ Dept Only | ❌ | ❌ |
| View Assigned Projects | ✅ | ✅ | ✅ | ✅ |
| Create Project Proposal | ❌ | ✅ | ❌ | ❌ |
| Approve/Reject Proposal | ✅ | ❌ | ❌ | ❌ |
| Create Project Directly | ❌ | ❌ | ❌ | ❌ |
| Manage Tasks | ✅ | ✅ | ✅ | ❌ |
| System Analytics | ✅ | ❌ | ❌ | ❌ |
| Department Analytics | ✅ | ✅ Own | ❌ | ❌ |
| Project Analytics | ✅ | ✅ Dept | ✅ Own | ✅ Assigned |
| Personal Analytics | ✅ | ✅ | ✅ | ✅ |

### Navigation by Role

| Role | Navbar Items |
|------|-------------|
| Admin | Dashboard / Departments / Proposals / Projects |
| Dept Head | Dashboard / Departments / Proposals / Projects |
| Project Lead | Dashboard / Projects |
| Collaboration | Dashboard / My Projects |

---

## 🔄 Project Proposal Workflow

Projects can no longer be created directly. The workflow is:

```
1. Dept Head → Create Proposal (title, description, lead, deadline)
2. Admin → Review Proposal
3a. Admin Approves → Project created automatically
3b. Admin Rejects → Proposal marked rejected with reason
```

**On Approval:** A `Project` instance is automatically created with the proposal's details. The proposal stores a link to the created project.

---

## 📊 Analytics System

### Endpoints

| Endpoint | Access | Description |
|----------|--------|-------------|
| `GET /api/analytics/user/` | All users | Personal task analytics |
| `GET /api/analytics/project/<id>/` | Project members+ | Project statistics |
| `GET /api/analytics/department/<id>/` | Dept Head + Admin | Department analytics |
| `GET /api/analytics/system/` | Admin only | System-wide statistics |

### Metrics Calculated

- **Completion Rate:** `completed_tasks / total_tasks * 100`
- **Efficiency Score:** `on_time_completed / total_completed * 100`
- **Overdue Tasks:** `deadline < today AND status != Completed`
- **Productivity Score:** `projects with >50% completion / total_projects * 100`

### Sample Response — User Analytics
```json
{
    "user_id": 1,
    "username": "admin",
    "total_tasks": 15,
    "completed_tasks": 10,
    "pending_tasks": 3,
    "in_progress_tasks": 2,
    "overdue_tasks": 1,
    "completion_rate": 66.67,
    "efficiency_score": 80.00
}
```

---

## 🗄 Database Models

### User (accounts)
- Extends `AbstractUser`
- `role`: admin / dept_head / project_lead / collaboration
- `department`: ForeignKey to Department

### Department (departments)
- `department_name`, `workspace_code` (unique), `department_head`, `created_at`

### Project (projects)
- `project_name`, `description`, `department`, `project_lead`, `members` (M2M), `deadline`, `created_at`

### ProjectProposal (projects)
- `title`, `description`, `department`, `proposed_by` (Dept Head)
- `status`: Pending / Approved / Rejected
- `proposed_project_lead`, `proposed_deadline`
- `created_project`: OneToOne link to Project (set on approval)
- `admin_notes`, `created_at`, `approved_at`, `rejected_at`

### Task (tasks)
- `title`, `description`, `project`, `assigned_to`, `deadline`
- `status`: Pending / In Progress / Completed
- `priority`: Low / Medium / High

### Message (chat)
- `project`, `sender`, `message_text`, `file_attachment`, `created_at`

---

## 🚀 Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/Piyush288a/NexuSphere.git
cd NexuSphere/nexusphere
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux
```

3. **Install Django**
```bash
pip install django
```

4. **Run migrations**
```bash
python manage.py migrate
```

5. **Load test data**
```bash
python create_comprehensive_test_data.py
```

6. **Start server**
```bash
python manage.py runserver
```

7. **Access the app**
- App: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

---

## 🔑 Test Credentials

All users login with: `workspace_code` + `username` + `password`

| Role | Workspace | Username | Password | Dashboard |
|------|-----------|----------|----------|-----------|
| Admin | CS | admin | admin123 | `/admin-dashboard/` |
| Dept Head (CS) | CS | dept_head_cs | dept123 | `/department-dashboard/` |
| Dept Head (MECH) | MECH | dept_head_mech | dept123 | `/department-dashboard/` |
| Project Lead (CS) | CS | project_lead_1 | lead123 | `/project-dashboard/` |
| Project Lead (MECH) | MECH | project_lead_2 | lead123 | `/project-dashboard/` |
| Collaboration (CS) | CS | member_cs_1 | member123 | `/dashboard/` |
| Collaboration (CS) | CS | member_cs_2 | member123 | `/dashboard/` |
| Collaboration (MECH) | MECH | member_mech_1 | member123 | `/dashboard/` |
| Collaboration (MECH) | MECH | member_mech_2 | member123 | `/dashboard/` |

---

## 🌐 URL Endpoints

### Authentication
| URL | Description |
|-----|-------------|
| `/` | Home → redirects to login or dashboard |
| `/login/` | Workspace-based login |
| `/logout/` | Logout → redirects to `/login/` |

### Dashboards
| URL | Role |
|-----|------|
| `/dashboard/` | Collaboration |
| `/admin-dashboard/` | Admin |
| `/department-dashboard/` | Dept Head |
| `/project-dashboard/` | Project Lead |

### Departments
| URL | Description |
|-----|-------------|
| `/departments/` | List all departments |
| `/departments/<id>/` | Department detail |

### Projects & Proposals
| URL | Description | Access |
|-----|-------------|--------|
| `/projects/` | List projects (filtered by role) | All |
| `/projects/<id>/` | Project detail | Members+ |
| `/projects/proposals/` | List proposals | Admin, Dept Head |
| `/projects/proposals/create/` | Create proposal | Dept Head only |
| `/projects/proposals/<id>/` | Proposal detail | Admin, Dept Head |
| `/projects/proposals/<id>/approve/` | Approve proposal | Admin only |
| `/projects/proposals/<id>/reject/` | Reject proposal | Admin only |

### Tasks
| URL | Description |
|-----|-------------|
| `/projects/<id>/tasks/` | Task list for project |
| `/projects/<id>/tasks/create/` | Create task |
| `/tasks/<id>/` | Task detail |
| `/tasks/<id>/update-status/` | Update task status |

### Chat
| URL | Description |
|-----|-------------|
| `/projects/<id>/chat/` | Project chat |

### Analytics APIs
| URL | Access |
|-----|--------|
| `/api/analytics/user/` | All users (own data) |
| `/api/analytics/project/<id>/` | Project members+ |
| `/api/analytics/department/<id>/` | Dept Head + Admin |
| `/api/analytics/system/` | Admin only |

### Admin Panel
| URL | Description |
|-----|-------------|
| `/admin/` | Django admin panel |

---

## 🔐 Security Features

- CSRF protection on all forms
- Password hashing (Django default)
- `@login_required` on all views
- Role validation before data access
- SQL injection protection (Django ORM)
- XSS protection (Django templates)
- 403 responses for unauthorized API access
- 404 responses for unauthorized resource access

---

## 🚀 Future Enhancements

- Real-time notifications with WebSockets
- Analytics charts and graphs in dashboards
- Email notifications for proposals and task assignments
- Calendar view for deadlines
- REST API for mobile app integration
- Two-factor authentication
- Dark mode toggle
- Export reports (PDF/Excel)

---

## 👥 Contributors

- **Piyush288a** — Core development, RBAC, Analytics, Proposal workflow
- **SmitBhalanii** — Phase 5.1 (Departments & Projects Views)
- **Darshan-Dalsaniya** — Phases 4–5 implementation
- GitHub: https://github.com/Piyush288a/NexuSphere
- Email: piyush288a@gmail.com

---

**Version:** 2.0.0  
**Last Updated:** March 28, 2026  
**Django:** 6.0.1 | **Python:** 3.13.0
