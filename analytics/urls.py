from django.urls import path
from . import views

urlpatterns = [
    path('user/', views.user_analytics, name='user_analytics'),
    path('project/<int:project_id>/', views.project_analytics, name='project_analytics'),
    path('department/<int:department_id>/', views.department_analytics, name='department_analytics'),
    path('system/', views.system_analytics, name='system_analytics'),
]
