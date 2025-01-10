from rest_framework import serializers
from accounts import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ['user', 'profile_img', 'fullName', 'age', 'phoneNumber', 'email', 'country', 'gender', 'Expenses', 'is_admin', 'is_modir']


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
    profile_img = serializers.ImageField(required=False, allow_null=True)
    profile_img_url = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = ['fullName', 'phoneNumber', 'email', 'user', 'profile_img', 'profile_img_url']

    def create(self, validated_data):
        # Ensure profile_img is set to the default if it's not provided
        if 'profile_img' not in validated_data:
            validated_data['profile_img'] = 'userProfile/default.png'
        return super().create(validated_data)

    def get_profile_img_url(self, obj):
        # If profile_img is null, return the default image URL
        if obj.profile_img:
            return obj.profile_img.url
        return '/userProfile/default.png'  # Default image URL




class AdminRegisterSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(required=False, allow_null=True)
    profile_img_url = serializers.SerializerMethodField()  # To return the image URL or default

    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'user', 'specialties', 'profile_img', 'is_admin', 'is_modir', 'profile_img_url']

    def create(self, validated_data):
        # Explicitly set 'is_admin' here if needed
        validated_data['is_admin'] = True
        
        # If no profile_img is provided, set it to the default value
        if 'profile_img' not in validated_data:
            validated_data['profile_img'] = 'userProfile/default.png'
        
        return super().create(validated_data)

    def get_profile_img_url(self, obj):
        # If profile_img exists, return its URL, otherwise return the default image URL
        if obj.profile_img:
            return obj.profile_img.url
        return '/userProfile/default.png'  # Default image URL




class AdminProfileUpdate(serializers.ModelSerializer):
    fullName = serializers.CharField(required=False)
    phoneNumber = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    experience_years = serializers.IntegerField(required=False, allow_null=True)
    profile_image = serializers.ImageField(required=False)  # Change from profile_img to profile_image

    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'experience_years', 'profile_image']

    def update(self, instance, validated_data):
        # Check if profile_image is in the validated data
        if 'profile_image' in validated_data:
            # Update profile_image if provided
            instance.profile_img = validated_data['profile_image']
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance



        
        
# class AdminUserProfileUpdate(serializers.ModelSerializer):
#     fullName = serializers.CharField(required=False)
#     phoneNumber = serializers.CharField(required=False)
#     email = serializers.EmailField(required=False)
#     experience_years = serializers.IntegerField(required=False, allow_null=True)
#     profile_img = serializers.ImageField(required=False)

#     class Meta:
#         model = models.UserProfile
#         fields = ['fullName', 'phoneNumber', 'email', 'profile_img']


        
class AdminProfileSerializer(serializers.ModelSerializer):
    profile_img = serializers.ImageField(required=False)
    class Meta:
        model = models.Specialist
        fields = ['fullName', 'phoneNumber', 'email', 'profile_img', 'experience_years', 'income', 'is_admin', 'is_modir']
        
        

class userprofileUpdateFromSerializer(serializers.ModelSerializer):
    fullName = serializers.CharField(required=False)
    profile_img = serializers.ImageField(required=False)
    class Meta:
        model = models.UserProfile
        fields = ['fullName', 'gender', 'email', 'profile_img']
        
        
        
class UserProfileUpdateFromSerializer2(serializers.ModelSerializer):
    fullName = serializers.CharField(required=False)
    phoneNumber = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    profile_img = serializers.ImageField(required=False)  # Model field name for profile image

    class Meta:
        model = models.UserProfile
        fields = ['fullName', 'phoneNumber', 'email', 'profile_img']

    def update(self, instance, validated_data):
        # Handle the profile_img update or retention
        if 'profile_image' in validated_data:
            instance.profile_img = validated_data['profile_image']
        else:
            validated_data['profile_image'] = instance.profile_img

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance