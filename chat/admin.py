from django.contrib import admin
from .models import Message


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('project', 'sender', 'message_preview', 'created_at')
    list_filter = ('project', 'created_at')
    search_fields = ('message_text',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)
    
    def message_preview(self, obj):
        return obj.message_text[:50] + '...' if len(obj.message_text) > 50 else obj.message_text
    message_preview.short_description = 'Message Preview'
