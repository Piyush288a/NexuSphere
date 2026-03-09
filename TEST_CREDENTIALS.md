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

### 2. Department Head (Computer Science)
- **Workspace Code:** `CS`
- **Username:** `dept_head_cs`
- **Password:** `dept123`
- **Role:** Department Head
- **Department:** Computer Science
- **Expected Redirect:** `/department-dashboard/`
- **Permissions:** Department management

### 3. Department Head (Mechanical)
- **Workspace Code:** `MECH`
- **Username:** `dept_head_mech`
- **Password:** `dept123`
- **Role:** Department Head
- **Department:** Mechanical
- **Expected Redirect:** `/department-dashboard/`
- **Permissions:** Department management

### 4. Project Lead (Computer Science)
- **Workspace Code:** `CS`
- **Username:** `project_lead_1`
- **Password:** `lead123`
- **Role:** Project Lead
- **Department:** Computer Science
- **Expected Redirect:** `/project-dashboard/`
- **Permissions:** Project management

### 5. Project Lead (Mechanical)
- **Workspace Code:** `MECH`
- **Username:** `project_lead_2`
- **Password:** `lead123`
- **Role:** Project Lead
- **Department:** Mechanical
- **Expected Redirect:** `/project-dashboard/`
- **Permissions:** Project management

### 6. Member (Computer Science - 1)
- **Workspace Code:** `CS`
- **Username:** `member_cs_1`
- **Password:** `member123`
- **Role:** Member
- **Department:** Computer Science
- **Expected Redirect:** `/dashboard/`
- **Permissions:** Basic access

### 7. Member (Computer Science - 2)
- **Workspace Code:** `CS`
- **Username:** `member_cs_2`
- **Password:** `member123`
- **Role:** Member
- **Department:** Computer Science
- **Expected Redirect:** `/dashboard/`
- **Permissions:** Basic access

### 8. Member (Mechanical - 1)
- **Workspace Code:** `MECH`
- **Username:** `member_mech_1`
- **Password:** `member123`
- **Role:** Member
- **Department:** Mechanical
- **Expected Redirect:** `/dashboard/`
- **Permissions:** Basic access

### 9. Member (Mechanical - 2)
- **Workspace Code:** `MECH`
- **Username:** `member_mech_2`
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

#### Test 2: Department Head (CS) Login
```
Workspace: CS
Username: dept_head_cs
Password: dept123
Expected: Redirect to /department-dashboard/
```

#### Test 3: Department Head (MECH) Login
```
Workspace: MECH
Username: dept_head_mech
Password: dept123
Expected: Redirect to /department-dashboard/
```

#### Test 4: Project Lead (CS) Login
```
Workspace: CS
Username: project_lead_1
Password: lead123
Expected: Redirect to /project-dashboard/
```

#### Test 5: Project Lead (MECH) Login
```
Workspace: MECH
Username: project_lead_2
Password: lead123
Expected: Redirect to /project-dashboard/
```

#### Test 6: Member (CS) Login
```
Workspace: CS
Username: member_cs_1
Password: member123
Expected: Redirect to /dashboard/
```

#### Test 7: Member (MECH) Login
```
Workspace: MECH
Username: member_mech_1
Password: member123
Expected: Redirect to /dashboard/
```

### ❌ Invalid Login Tests

#### Test 8: Invalid Workspace
```
Workspace: INVALID
Username: admin
Password: admin123
Expected Error: "Workspace not found."
```

#### Test 9: Invalid Credentials
```
Workspace: CS
Username: admin
Password: wrongpassword
Expected Error: "Invalid username or password."
```

#### Test 10: Wrong Workspace for User
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
   - Department Head: dept_head_cs
   - Members: 5 users (1 admin, 1 dept_head, 1 project_lead, 2 members)

2. **Mechanical** (Workspace: MECH)
   - Department Head: dept_head_mech
   - Members: 4 users (1 dept_head, 1 project_lead, 2 members)

### Projects

Projects can be created by admin, department heads, and project leads through the web interface.

### Tasks

Tasks can be created within projects and assigned to team members.

---

## Testing Checklist

### Authentication Tests
- [ ] Login with admin credentials
- [ ] Login with dept_head_cs credentials
- [ ] Login with dept_head_mech credentials
- [ ] Login with project_lead_1 credentials
- [ ] Login with project_lead_2 credentials
- [ ] Login with member_cs_1 credentials
- [ ] Login with member_mech_1 credentials
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
- [ ] Admin dashboard displays system statistics
- [ ] Department dashboard displays department data
- [ ] Project dashboard displays led projects
- [ ] Member dashboard shows personal tasks
- [ ] Member dashboard shows assigned projects
- [ ] Member dashboard shows upcoming deadlines

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
- **Users:** 9
- **Projects:** Created via web interface
- **Tasks:** Created via web interface
- **Messages:** Created via web interface

---

## Quick Commands

### Start Server
```bash
python manage.py runserver
```

### Check Current Users
```bash
python check_users.py
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
- Workspace codes are case-sensitive (CS, MECH)
- Each department now has its own department head and project lead
- Multiple members per department for better testing scenarios

---

**Last Updated:** March 9, 2026  
**System Status:** ✅ All users configured successfully
