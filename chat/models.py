from django.db import models

class Message(models.Model):
    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='sent_messages'
    )
    message_text = models.TextField()
    file_attachment = models.FileField(
        upload_to='chat_files/',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        # PART 13 — composite index for fast per-project history queries
        indexes = [
            models.Index(fields=['project', 'created_at'], name='chat_project_created_idx'),
        ]
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} - {self.project}"
