from django.db import models
from core.models import AbstractTimeStamped


class Conversation(AbstractTimeStamped):

    participants = models.ManyToManyField(
        "users.User", blank=True, related_name="conversations"
    )

    def __str__(self):
        return str(self.created)


class Message(AbstractTimeStamped):

    message = models.TextField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="messages"
    )
    conversation = models.ForeignKey(
        "Conversation", on_delete=models.CASCADE, related_name="messages"
    )

    def __str__(self):
        return f"{self.user} says: {self.message}"
