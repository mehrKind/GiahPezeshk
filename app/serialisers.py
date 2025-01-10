from rest_framework import serializers
from . import models


class DailyTextSerialiser(serializers.ModelSerializer):
    class Meta:
        model = models.DailyTextModel
        fields = "__all__"
        
        
