from django.db import models

class Department(models.Model):
    department_name = models.CharField(max_length=200)
    workspace_code = models.CharField(max_length=20, unique=True, default='TEMP')
    department_head = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='headed_departments'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.department_name} ({self.workspace_code})"
