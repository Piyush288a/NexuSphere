from django.urls import path
from . import views
from tasks import views as task_views
from chat import views as chat_views

urlpatterns = [
    path('', views.projects_list, name='projects_list'),
    path('my-projects/', views.my_projects, name='my_projects'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/manage-team/', views.manage_team, name='manage_team'),

    # Project Proposals
    path('proposals/', views.proposal_list, name='proposal_list'),
    path('proposals/create/', views.proposal_create, name='proposal_create'),
    path('proposals/<int:proposal_id>/', views.proposal_detail, name='proposal_detail'),
    path('proposals/<int:proposal_id>/approve/', views.proposal_approve, name='proposal_approve'),
    path('proposals/<int:proposal_id>/reject/', views.proposal_reject, name='proposal_reject'),

    # Tasks
    path('<int:project_id>/tasks/', task_views.task_list, name='task_list'),
    path('<int:project_id>/tasks/create/', task_views.task_create, name='task_create'),

    # Chat
    path('<int:project_id>/chat/', chat_views.project_chat, name='project_chat'),
]
