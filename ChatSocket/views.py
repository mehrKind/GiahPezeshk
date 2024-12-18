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
                "room_users" : users
            }
        )
        # return request
        return Response(room_id, status=status.HTTP_201_CREATED)
    

class ChatUsers(APIView):
    permission_classes = [AllowAny]

    def get(self, request,username):
        chats = collection.find({"room_users": username},{'messages': 0,'_id': 0}) 
        return Response(list(chats), status=status.HTTP_200_OK)