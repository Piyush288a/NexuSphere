from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_login, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('department-dashboard/', views.department_dashboard, name='department_dashboard'),
    path('project-dashboard/', views.project_dashboard, name='project_dashboard'),
    path('my-tasks/', views.my_tasks, name='my_tasks'),
    path('my-deadlines/', views.my_deadlines, name='my_deadlines'),
]
