# NexuSphere Test Credentials

## Quick Access

**Server URL:** http://127.0.0.1:8000/  
**Login Page:** http://127.0.0.1:8000/login/  
**Admin Panel:** http://127.0.0.1:8000/admin/

---

## Test User Accounts

### 1. Admin User
- **Workspace Code:** `CS`
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Admin
- **Department:** Computer Science
- **Expected Redirect:** `/admin-dashboard/`
- **Permissions:** Full system access, superuser

### 2. Department Head
- **Workspace Code:** `CS`
- **Username:** `dept_head`
- **Password:** `dept123`
- **Role:** Department Head
- **Department:** Computer Science
- **Expected Redirect:** `/department-dashboard/`
- **Permissions:** Department management

### 3. Project Lead
- **Workspace Code:** `CS`
- **Username:** `project_lead`
- **Password:** `lead123`
- **Role:** Project Lead
- **Department:** Computer Science
- **Expected Redirect:** `/project-dashboard/`
- **Permissions:** Project management
- **Projects:** AI Attendance System, Student Portal Redesign

### 4. Member (Computer Science)
- **Workspace Code:** `CS`
- **Username:** `member_cs`
- **Password:** `member123`
- **Role:** Member
- **Department:** Computer Science
- **Expected Redirect:** `/dashboard/`
- **Permissions:** Basic access
- **Assigned Tasks:** 3 tasks

### 5. Member (Mechanical)
- **Workspace Code:** `MECH`
- **Username:** `member_mech`
- **Password:** `member123`
- **Role:** Member
- **Department:** Mechanical
- **Expected Redirect:** `/dashboard/`
- **Permissions:** Basic access

---

## Test Scenarios

### ✅ Valid Login Tests

#### Test 1: Admin Login
```
Workspace: CS
Username: admin
Password: admin123
Expected: Redirect to /admin-dashboard/
```

#### Test 2: Department Head Login
```
Workspace: CS
Username: dept_head
Password: dept123
Expected: Redirect to /department-dashboard/
```

#### Test 3: Project Lead Login
```
Workspace: CS
Username: project_lead
Password: lead123
Expected: Redirect to /project-dashboard/
```

#### Test 4: Member Login
```
Workspace: CS
Username: member_cs
Password: member123
Expected: Redirect to /dashboard/
```

### ❌ Invalid Login Tests

#### Test 5: Invalid Workspace
```
Workspace: INVALID
Username: admin
Password: admin123
Expected Error: "Workspace not found."
```

#### Test 6: Invalid Credentials
```
Workspace: CS
Username: admin
Password: wrongpassword
Expected Error: "Invalid username or password."
```

#### Test 7: Wrong Workspace for User
```
Workspace: MECH
Username: admin
Password: admin123
Expected Error: "Invalid workspace for this user."
```

---

## Sample Data Created

### Departments
1. **Computer Science** (Workspace: CS)
   - Department Head: dept_head
   - Members: 4 users

2. **Mechanical** (Workspace: MECH)
   - Department Head: Not assigned
   - Members: 1 user

### Projects

#### 1. AI Attendance System
- **Department:** Computer Science
- **Project Lead:** project_lead
- **Members:** project_lead, member_cs
- **Deadline:** 90 days from today
- **Description:** Develop an AI-powered attendance tracking system using facial recognition
- **Tasks:** 3 tasks
- **Messages:** 2 messages

#### 2. Student Portal Redesign
- **Department:** Computer Science
- **Project Lead:** project_lead
- **Members:** member_cs
- **Deadline:** 60 days from today
- **Description:** Modernize the student portal with improved UI/UX
- **Tasks:** 1 task
- **Messages:** 1 message

### Tasks

#### Project: AI Attendance System
1. **Build Login UI**
   - Assigned to: member_cs
   - Status: Pending
   - Priority: Medium
   - Deadline: 14 days

2. **Setup Database Schema**
   - Assigned to: project_lead
   - Status: In Progress
   - Priority: High
   - Deadline: 7 days

3. **Implement Facial Recognition**
   - Assigned to: member_cs
   - Status: Pending
   - Priority: High
   - Deadline: 30 days

#### Project: Student Portal Redesign
4. **Design Dashboard Mockups**
   - Assigned to: member_cs
   - Status: Completed
   - Priority: Medium
   - Deadline: 10 days

---

## Testing Checklist

### Authentication Tests
- [ ] Login with admin credentials
- [ ] Login with dept_head credentials
- [ ] Login with project_lead credentials
- [ ] Login with member credentials
- [ ] Test invalid workspace error
- [ ] Test invalid credentials error
- [ ] Test wrong workspace error
- [ ] Test logout functionality
- [ ] Verify protected route redirects

### Role-Based Redirect Tests
- [ ] Admin redirects to /admin-dashboard/
- [ ] Dept Head redirects to /department-dashboard/
- [ ] Project Lead redirects to /project-dashboard/
- [ ] Member redirects to /dashboard/

### Dashboard Tests
- [ ] Admin dashboard displays user info
- [ ] Department dashboard displays user info
- [ ] Project dashboard displays user info
- [ ] Member dashboard shows statistics
- [ ] Member dashboard shows assigned tasks
- [ ] Member dashboard shows recent projects

### Admin Panel Tests
- [ ] Access admin panel with admin credentials
- [ ] View all departments
- [ ] View all users
- [ ] View all projects
- [ ] View all tasks
- [ ] View all messages
- [ ] Create new records
- [ ] Edit existing records

---

## Database Statistics

- **Departments:** 2
- **Users:** 5
- **Projects:** 2
- **Tasks:** 4
- **Messages:** 3

---

## Quick Commands

### Start Server
```bash
python manage.py runserver
```

### Create Test Data
```bash
python create_comprehensive_test_data.py
```

### Access Admin Panel
```bash
# Login with admin credentials
http://127.0.0.1:8000/admin/
Username: admin
Password: admin123
```

---

## Notes

- All passwords are set to simple values for testing purposes
- In production, use strong passwords and proper security measures
- Test data can be regenerated by running `create_comprehensive_test_data.py`
- The script clears existing test data before creating new records
- Workspace codes are case-sensitive (CS, MECH)

---

**Last Updated:** March 8, 2026  
**System Status:** ✅ All test data created successfully
