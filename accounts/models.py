from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    GENDER_TYPE = (
         ("مرد", "مرد"),
         ("زن", "زن")
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_img = models.ImageField(upload_to="userProfile/", blank=True, default="userProfile/default.png")
    fullName = models.CharField(max_length=255)
    age = models.PositiveIntegerField(blank=True, null=True)    
    phoneNumber = models.CharField(max_length=11, blank=True)
    email = models.EmailField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=True)
    gender = models.CharField(choices=GENDER_TYPE, max_length=100, blank=True)
    Expenses = models.BigIntegerField(default=0)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s profile"
    def save(self, *args, **kwargs):
        # Set is_admin based on whether the user is a Specialist
        if hasattr(self, 'specialist'):
            self.is_admin = True
        else:
            self.is_admin = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Speciality(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Specialist(UserProfile):
    position = models.CharField(max_length=255, default="عضو هیئت علمی دانشگاه جهرم")
    specialties = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    experience_years = models.PositiveIntegerField(blank=True, null=True)
    income = models.BigIntegerField(default=0)

    def __str__(self):
        return f"{self.fullName} - {self.position}"

# # Signal to create UserProfile when User is created
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)