import json
from channels.generic.websocket import AsyncWebsocketConsumer
from pymongo import MongoClient
from bson import ObjectId
from django.conf import settings
import datetime

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
        
        chat_history = collection.find_one({"room_name": self.room_name}) 
        if chat_history == None:
            await self.close()
            return
        else:
            if not (self.username in chat_history['room_users']):
                await self.close()
                return

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Load chat history from MongoDB
        
        if chat_history and "messages" in chat_history:
            for message in chat_history["messages"]:
                await self.send(text_data=json.dumps({
                    "msg_type" : message["msg_type"],
                    "username": message["username"],
                    "message": message["message"],
                    "date_time" : message["date_time"].isoformat()
                }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        msg_type = text_data_json.get("msg_type")
        if not message:
            return
        

        # Save message to MongoDB
        collection.update_one(
            {"room_name": self.room_name},
            {"$push": {"messages": {"msg_type":msg_type,"username": self.username, "message": message, "date_time": datetime.datetime.now(datetime.timezone.utc)}}},
            upsert=True
        )


        
        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "msg_type": msg_type,
                "message": message,
                "username": self.username,
                "date_time": datetime.datetime.now(datetime.timezone.utc)
            }
        )


        


    async def chat_message(self, event):
        message = event["message"]
        msg_type = event["msg_type"]
        username = event["username"]
        date_time = event['date_time'].isoformat()
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "username": username,
            "msg_type": msg_type,
            "message": message,
            "date_time": date_time
        }))
