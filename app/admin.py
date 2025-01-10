from django.contrib import admin
from . import models

class DailyTextAdmin(admin.ModelAdmin):
    # list_display = ("user__id", ")
    
    class Meta:
        model = models.DailyTextModel
        fields = "__all__"

admin.site.register(models.DailyTextModel, DailyTextAdmin)
