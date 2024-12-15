from rest_framework import serializers
from accounts import models


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['user', 'profile_img', 'fullName', 'age', 'phoneNumber', 'email', 'country', 'gender', 'Expenses']

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['profile_img', 'fullName', 'age', 'phoneNumber', 'email', 'country', 'gender', 'Expenses']



class SpecialistProfileSerializer(serializers.ModelSerializer):
    last_login = serializers.DateTimeField(source='user.last_login', read_only=True)

    class Meta:
        model = models.Specialist
        fields = [
            'user', 'profile_img', 'fullName', 'age', 'phoneNumber',
            'email', 'country', 'gender', 'position', 'specialties',
            'experience_years', 'last_login'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['fullName', 'phoneNumber', 'email', 'user']
        
class AdminRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'user', 'specialties', 'profile_img']
        

class AdminProfileUpdate(serializers.ModelSerializer):
    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'experience_years', 'profile_img']
        
        
class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'profile_img', 'experience_years', 'income', 'is_admin']