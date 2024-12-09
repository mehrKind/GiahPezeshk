from rest_framework import serializers
from accounts import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['user', 'profile_img', 'fullName', 'age', 'phoneNumber', 'email', 'country', 'gender']



class SpecialistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialist
        fields = ['user', 'profile_img', 'fullName', 'age', 'phoneNumber', 'email', 'country', 'gender', 'position', 'specialties', 'experience_years']


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['fullName', 'phoneNumber', 'email', 'user']