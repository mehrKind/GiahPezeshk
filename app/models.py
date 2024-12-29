from django.db import models
from accounts.models import UserProfile

class DailyTextModel(models.Model):
    authors = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True)
    content_img = models.ImageField(upload_to="daily_img/", blank=True, null=True)
    content = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or "Untitled"

    class Meta:
        ordering = ['-date_created']
        verbose_name = "Daily Text"
        verbose_name_plural = "Daily Texts"
