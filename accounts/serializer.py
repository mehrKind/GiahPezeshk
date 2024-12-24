from rest_framework import serializers
from accounts import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['user', 'profile_img', 'fullName', 'age', 'phoneNumber', 'email', 'country', 'gender', 'Expenses', 'is_admin']


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
        fields = ['fullName', 'phoneNumber', 'email', 'user', 'specialties', 'profile_img', 'is_admin']
        

class AdminProfileUpdate(serializers.ModelSerializer):
    user_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'experience_years', 'profile_img', 'user_password']

    def update(self, instance, validated_data):
        # Extract the user password if provided
        user_password = validated_data.pop('user_password', None)

        # Update the Specialist instance
        instance.fullName = validated_data.get('fullName', instance.fullName)
        instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
        instance.email = validated_data.get('email', instance.email)
        instance.experience_years = validated_data.get('experience_years', instance.experience_years)
        instance.profile_img = validated_data.get('profile_img', instance.profile_img)
        instance.save()

        # Update the User password if provided
        if user_password:
            user = instance.user
            user.password = make_password(user_password)  # Hash the new password
            user.save()

        return instance
        
class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'profile_img', 'experience_years', 'income', 'is_admin']
        
        

class userprofileUpdateFromSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(required=False)
    class Meta:
        model = models.UserProfile
        fields = ['fullName', 'gender', 'email', 'profile_img']
        