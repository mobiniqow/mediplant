# your_app_name/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from .models import DoctorVisitChat
from .serializers import DoctorVisitChatSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.doctor_visit_id = self.scope['url_route']['kwargs']['doctor_visit_id']
        self.room_group_name = f"chat_{self.doctor_visit_id}"

        # اتصالی که برای doctor_visit_id خاص است را ایجاد می‌کنیم
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # اجازه دادن به WebSocket برای اتصال
        await self.accept()

    async def disconnect(self, close_code):
        # قطع اتصال زمانی که WebSocket بسته می‌شود
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # دریافت پیام از WebSocket
        data = json.loads(text_data)
        message = data['message']
        user_id = data['user_id']

        # ذخیره پیام به پایگاه داده
        chat_message = DoctorVisitChat.objects.create(
            doctor_id=self.doctor_visit_id,
            content=message,
            is_doctor=False,  # اگر از طرف پزشک نباشد
        )

        chat_message_serialized = DoctorVisitChatSerializer(chat_message).data

        # ارسال پیام به گروه WebSocket
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': chat_message_serialized['content'],
                'is_doctor': chat_message_serialized['is_doctor'],
                'created_at': chat_message_serialized['created_at'],
                'media_url': chat_message_serialized['media'],
            }
        )

    # برای ارسال پیام به WebSocket از این متد استفاده می‌کنیم
    async def chat_message(self, event):
        message = event['message']
        is_doctor = event['is_doctor']
        created_at = event['created_at']
        media_url = event['media_url']

        # ارسال پیام به WebSocket به کلاینت
        await self.send(text_data=json.dumps({
            'message': message,
            'is_doctor': is_doctor,
            'created_at': created_at,
            'media_url': media_url,
        }))
