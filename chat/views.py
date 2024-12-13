from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class MessageHistoryView(APIView):
    def get(self, request, room_name):
        messages = Message.objects.filter(room_name=room_name).order_by('timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
