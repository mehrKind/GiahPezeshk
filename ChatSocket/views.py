from django.shortcuts import render
import uuid
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["chat_app"]  # Database name
collection = db["room"]

def index(request):
    return render(request, "chat/index.html")


def room(request, room_name,user_name):
    return render(request, "chat/room.html", {"room_name": room_name,"username":user_name})

def create_room(request):
    room_id = str(uuid.uuid1())  # Convert UUID to string
    print(room_id)
    collection.insert_one(
        {"room_name": room_id.replace('-','')}
    )
    # return request
    return Response(room_id, status=status.HTTP_201_CREATED)