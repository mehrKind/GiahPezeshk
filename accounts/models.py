from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_TYPE = (
         ("مرد", "مرد"),
         ("زن", "زن")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="userProfile/", blank=True, default="userProfile/default.jpg")
    fullName = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=True, null=True)    
    phoneNumber = models.CharField(max_length=11, blank=True)
    email = models.EmailField(max_length=255)
    country = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER_TYPE, max_length=100)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Speciality(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Specialist(UserProfile):
    position = models.CharField(max_length=255)
    specialties = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.fullName} - {self.position}"
