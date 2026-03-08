from django.urls import path
from . import views

urlpatterns = [
    path('<int:task_id>/', views.task_detail, name='task_detail'),
    path('<int:task_id>/update-status/', views.task_update_status, name='task_update_status'),
]
