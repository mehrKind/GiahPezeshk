from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serialisers

class DailyTextView(APIView):
    def get(self, request):
        texts = models.DailyTextModel.objects.all().order_by("-date_created")[:5]
        text_serializer = serialisers.DailyTextSerialiser(texts, many=True)

        context = {
            "status": 200,
            "data": text_serializer.data,
            "error": None
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request):
        text_serializer = serialisers.DailyTextSerialiser(data=request.data)
        if text_serializer.is_valid():
            text_serializer.save()
            return Response({
                "status": 201,
                "data": text_serializer.data,
                "error": None
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "status": 400,
                "data": None,
                "error": text_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
