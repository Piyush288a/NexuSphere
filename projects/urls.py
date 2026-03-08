from django.urls import path
from . import views
from tasks import views as task_views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/tasks/', task_views.task_list, name='task_list'),
    path('<int:project_id>/tasks/create/', task_views.task_create, name='task_create'),
]
