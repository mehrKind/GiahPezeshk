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
        
        # Fetch chat history from MongoDB
        chat_history = collection.find_one({"room_name": self.room_name})

        if chat_history is None:
            await self.close()
            return
        else:
            if self.username not in chat_history['room_users']:
                await self.close()
                return

        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Load chat history from MongoDB
        if chat_history and "messages" in chat_history:
            for message in chat_history["messages"]:
                # Ensure the message has an `_id` field
                if "_id" not in message:
                    message["_id"] = ObjectId()  # Generate a new ID if missing
                await self.send(text_data=json.dumps({
                    "msg_type": message["msg_type"],
                    "username": message["username"],
                    "message": message["message"],
                    "date_time": message["date_time"].isoformat(),
                    "seen": message.get("seen", False),  # Include seen status
                    "message_id": str(message["_id"])  # Include message_id
                }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        msg_type = text_data_json.get("msg_type")
        action = text_data_json.get("action")  # New field to handle actions like "seen"

        if action == "seen":
            # Handle seen action
            message_id = text_data_json.get("message_id")
            if message_id:
                await self.mark_message_as_seen(message_id)
            return

        if not message:
            return

        # Save message to MongoDB
        new_message = {
            "_id": ObjectId(),  # Generate a unique ID for the message
            "msg_type": msg_type,
            "username": self.username,
            "message": message,
            "date_time": datetime.datetime.now(datetime.timezone.utc),
            "seen": False  # Initialize seen as False
        }

        collection.update_one(
            {"room_name": self.room_name},
            {"$push": {"messages": new_message}},
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
                "date_time": new_message["date_time"],
                "seen": new_message["seen"],  # Include seen status
                "message_id": str(new_message["_id"])  # Include message_id
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        msg_type = event["msg_type"]
        username = event["username"]
        date_time = event['date_time'].isoformat()
        seen = event.get("seen", False)
        message_id = event.get("message_id")  # Include message_id

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "username": username,
            "msg_type": msg_type,
            "message": message,
            "date_time": date_time,
            "seen": seen,
            "message_id": message_id  # Include message_id
        }))

    async def mark_message_as_seen(self, message_id):
        """
        Mark a message as seen by the other side.
        """
        # Update the seen field for the specific message
        collection.update_one(
            {"room_name": self.room_name, "messages._id": ObjectId(message_id)},
            {"$set": {"messages.$.seen": True}}
        )

        # Notify the group that the message has been seen
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "message_seen",
                "message_id": message_id,
                "seen": True
            }
        )

    async def message_seen(self, event):
        """
        Notify the group that a message has been seen by the other side.
        """
        message_id = event["message_id"]
        seen = event["seen"]

        # Send the seen update to the WebSocket
        await self.send(text_data=json.dumps({
            "action": "seen",
            "message_id": message_id,
            "seen": seen
        }))