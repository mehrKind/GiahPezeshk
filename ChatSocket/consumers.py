import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.username = self.scope["url_route"]["kwargs"].get("username")

        # Ensure both username and room_name are provided
        if not self.room_name or not self.username:
            await self.close()
            return

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        if not message:
            return  # Ignore invalid messages

        # Include the username in the message
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": message, "username": self.username},
        )
        print(self.username,message)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"username": username, "message": message}))
