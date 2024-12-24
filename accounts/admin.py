from django.contrib import admin
from accounts import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user__id", "user", "gender", "fullName", "phoneNumber")
    search_fields = ["fullName", "user__username"]
    list_editable = ["phoneNumber"]
    list_display_links = ["user"]
    
    class Meta:
        model = models.UserProfile
        fields = "__all__"

admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Specialist)
admin.site.register(models.Speciality)
