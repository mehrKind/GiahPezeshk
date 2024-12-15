import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["chat_app"]  # Database name
collection = db["room"]  # Collection name

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.username = self.scope["url_route"]["kwargs"]["username"]

        if not self.room_name or not self.username:
            await self.close()
            return

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Load chat history from MongoDB
        chat_history = collection.find_one({"room_name": self.room_name})
        if chat_history and "messages" in chat_history:
            for message in chat_history["messages"]:
                await self.send(text_data=json.dumps({
                    "username": message["username"],
                    "message": message["message"],
                }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")

        if not message:
            return

        # Save message to MongoDB
        collection.update_one(
            {"room_name": self.room_name},
            {"$push": {"messages": {"username": self.username, "message": message}}},
            upsert=True
        )

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message,
                "username": self.username,
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "username": username,
            "message": message,
        }))
