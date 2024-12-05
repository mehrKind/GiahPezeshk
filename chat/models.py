from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

# class ChatRoom(models.Model):
#     name = models.CharField(max_length=255, unique=True, blank=True, null=True)
#     is_group = models.BooleanField(default=False)
#     participants = models.ManyToManyField(User, related_name="chatrooms")

#     def __str__(self):
#         return self.name or f"Room {self.id}"

# class Message(models.Model):
#     chatroom = models.ForeignKey(ChatRoom, related_name="messages", on_delete=models.CASCADE)
#     sender = models.ForeignKey(User, related_name="messages_sent", on_delete=models.CASCADE)
#     text = models.TextField(blank=True, null=True)
#     timestamp = models.DateTimeField(default=now)
#     is_read = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Message by {self.sender} in {self.chatroom}"

