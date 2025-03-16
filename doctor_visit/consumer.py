# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # یک نام برای گروه ایجاد کنید
        self.room_name = "chat_room"
        self.room_group_name = f"chat_{self.room_name}"

        # پیوستن به گروه
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # ترک کردن گروه هنگام قطع اتصال
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # دریافت پیام از WebSocket
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json['message']

        # ارسال پیام به گروه
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # دریافت پیام از گروه
    async def chat_message(self, event):
        message = event['message']

        # ارسال پیام به WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
