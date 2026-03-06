from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='projects'
    )
    project_lead = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='leading_projects'
    )
    members = models.ManyToManyField(
        'accounts.User',
        related_name='project_members'
    )
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.project_name
