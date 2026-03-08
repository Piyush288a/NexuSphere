from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
]
