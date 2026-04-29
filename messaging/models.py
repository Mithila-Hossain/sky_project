# Author: Mithila
# Used by: Ghoufran
# Description: Defines the Message model used for storing messages in the database


from django.db import models
from django.contrib.auth.models import User
from teams.models import Team

class Message(models.Model):
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Sent")
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.SET_NULL)

    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} → {self.receiver.username}"
