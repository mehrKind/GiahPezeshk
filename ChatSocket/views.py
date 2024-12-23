from django.shortcuts import render
import uuid
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from pymongo import MongoClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated ,AllowAny
import json
from datetime import datetime,timedelta


client = MongoClient("mongodb://localhost:27017/")
db = client["chat_app"]  # Database name
collection = db["room"]

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name,user_name):
    return render(request, "chat/room.html", {"room_name": room_name,"username":user_name})



class ProtectedView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)
        room_id = str(uuid.uuid1())  # Convert UUID to string
        users = data.get("users")
        collection.insert_one(
            {
                "room_name": room_id.replace('-',''),
                "room_users" : users,
                "is_open" : True
            }
        )
        # return request
        return Response(room_id.replace('-',''), status=status.HTTP_201_CREATED)
    

class ChatUsers(APIView):
    permission_classes = [AllowAny]

    def get(self, request,username):
        # chats = collection.find({"room_users": username},{'messages': 0,'_id': 0})
        chats = collection.find(
            {"room_users": username},  # Query filter
            {"messages": {"$slice": -1}, "_id": 0, "room_users": 1,"room_name":1}  # Projection

        )
        chats = list(chats)
        for chat in chats:
            chat['room_users'].remove(username)
        return Response(chats, status=status.HTTP_200_OK)
    

class ChangeAdmin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)
        room_name = data.get("room_name")
        user_to_change = data.get("user_to_change")
        new_user = data.get("new_user")
        filter_query = {"room_name":room_name,"room_users" : user_to_change}
        update_operation = {
            "$set":{
                "room_users.$":new_user
            }
        }
        result = collection.update_one(filter_query,update_operation)
        if result.modified_count == 1:
            return Response("ok", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Bad Request" , status=status.HTTP_400_BAD_REQUEST)
        


class ChangeClose(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = json.loads(request.body)
        print(data)
        room_name = data.get("room_name")
        is_open = data.get("is_open")
        filter_query = {"room_name":room_name}
        update_operation = {
            "$set":{
                "is_open":is_open
            }
        }
        result = collection.update_one(filter_query,update_operation)
        if result.modified_count == 1:
            return Response("ok", status=status.HTTP_202_ACCEPTED)
        else:
            return Response("Bad Request" , status=status.HTTP_400_BAD_REQUEST)
        


class UserMessagesCount(APIView):
    permission_classes = [AllowAny]

    def get(self, request,username):
        last_week = datetime.now() - timedelta(weeks=1)
        count = collection.aggregate([
            {
                '$unwind': '$messages'  # Flatten the messages array
            },
            {
                '$match': {
                    'messages.username': username,  # Match the user ID in the messages
                    'messages.date_time': {'$gte': last_week}  # Match the time range
                }
            },
            {
                '$count': 'comment_count'  # Count the documents that match
            }
        ])
        
        # Extract the count
        # total_messages = result[0]['total_messages'] if result else 0
        return Response(list(count)[0], status=status.HTTP_200_OK)
    