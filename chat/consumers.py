import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for project-based real-time chat.
    Room name: project_<project_id>
    """

    # ── Connect ──────────────────────────────────────────────────────────────
    async def connect(self):
        self.project_id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = f'project_{self.project_id}'
        self.user = self.scope['user']

        # Reject unauthenticated connections immediately
        if not self.user.is_authenticated:
            await self.close(code=4001)
            return

        # PART 12 — verify user belongs to this project
        if not await self.user_has_access():
            await self.close(code=4003)
            return

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Send last 50 messages on connect (PART 11)
        history = await self.get_message_history()
        await self.send(text_data=json.dumps({
            'type': 'history',
            'messages': history,
        }))

    # ── Disconnect ────────────────────────────────────────────────────────────
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # ── Receive from WebSocket ────────────────────────────────────────────────
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except (json.JSONDecodeError, ValueError):
            return

        message_text = data.get('message', '').strip()
        if not message_text:
            return

        # Save to DB and get back the saved instance
        saved = await self.save_message(message_text)

        # Broadcast to all group members (PART 7)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': saved['message'],
                'sender': saved['sender'],
                'sender_initial': saved['sender_initial'],
                'timestamp': saved['timestamp'],
                'message_id': saved['message_id'],
            }
        )

    # ── Broadcast handler (called for every member in group) ─────────────────
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'sender': event['sender'],
            'sender_initial': event['sender_initial'],
            'timestamp': event['timestamp'],
            'message_id': event['message_id'],
        }))

    # ── DB helpers (run in thread pool) ──────────────────────────────────────
    @database_sync_to_async
    def user_has_access(self):
        """PART 12 & 14 — check project membership."""
        from projects.models import Project
        try:
            project = Project.objects.select_related('department', 'project_lead').get(
                id=self.project_id
            )
        except Project.DoesNotExist:
            return False

        user = self.user
        if user.role == 'admin':
            return True
        if user.role == 'dept_head' and user.department == project.department:
            return True
        if project.project_lead == user:
            return True
        if project.members.filter(pk=user.pk).exists():
            return True
        return False

    @database_sync_to_async
    def save_message(self, message_text):
        """PART 6 — persist message and return serialisable dict."""
        from chat.models import Message
        msg = Message.objects.create(
            project_id=self.project_id,
            sender=self.user,
            message_text=message_text,
        )
        return {
            'message_id': msg.id,
            'message': msg.message_text,
            'sender': msg.sender.username,
            'sender_initial': msg.sender.username[0].upper(),
            'timestamp': msg.created_at.strftime('%b %d, %Y %I:%M %p'),
        }

    @database_sync_to_async
    def get_message_history(self):
        """PART 11 & 13 — last 50 messages, ordered oldest-first."""
        from chat.models import Message
        qs = (
            Message.objects
            .filter(project_id=self.project_id)
            .select_related('sender')
            .order_by('-created_at')[:50]
        )
        return [
            {
                'message_id': m.id,
                'message': m.message_text,
                'sender': m.sender.username if m.sender else 'Unknown',
                'sender_initial': (m.sender.username[0].upper() if m.sender else '?'),
                'timestamp': m.created_at.strftime('%b %d, %Y %I:%M %p'),
                'has_attachment': bool(m.file_attachment),
                'attachment_url': m.file_attachment.url if m.file_attachment else None,
                'attachment_name': m.file_attachment.name.split('/')[-1] if m.file_attachment else None,
            }
            for m in reversed(list(qs))
        ]
