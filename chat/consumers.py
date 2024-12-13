import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from .serializers import MessageSerializer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        serializer = MessageSerializer(data={
            'room_name': self.room_name,
            'sender': data['sender'],  # Sender should be provided in the WebSocket data
            'content': data['message']
        })

        if serializer.is_valid():
            # Save message to database
            serializer.save()

            # Broadcast the message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': serializer.data
                }
            )
        else:
            # Send validation errors back
            await self.send(text_data=json.dumps({
                'error': serializer.errors
            }))

    async def chat_message(self, event):
        # Broadcast the message to WebSocket clients
        await self.send(text_data=json.dumps(event['message']))
