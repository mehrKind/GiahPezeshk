from django.contrib import admin
from accounts import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "gender", "fullName", "phoneNumber")
    search_fields = ["fullName", "user__username"]
    list_editable = ["phoneNumber"]
    
    class Meta:
        model = models.UserProfile
        fields = "__all__"

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Specialist)
admin.site.register(models.Speciality)
