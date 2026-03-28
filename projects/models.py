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


class ProjectProposal(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(
        'departments.Department',
        on_delete=models.CASCADE,
        related_name='project_proposals'
    )
    proposed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='proposed_projects'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    # Fields for project creation upon approval
    proposed_project_lead = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='proposed_as_lead'
    )
    proposed_deadline = models.DateField()
    
    # Link to created project (if approved)
    created_project = models.OneToOneField(
        'Project',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='source_proposal'
    )
    
    def __str__(self):
        return f"{self.title} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
