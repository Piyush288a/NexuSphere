from django.contrib import admin
from django.urls import path, include
from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', account_views.custom_login, name='login'),
    path('logout/', account_views.custom_logout, name='logout'),
    path('departments/', include('departments.urls')),
    path('projects/', include('projects.urls')),
    path('', include('accounts.urls')),
]
