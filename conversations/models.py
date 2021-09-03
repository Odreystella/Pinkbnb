from django.db import models
from core.models import AbstractTimeStamped


class Conversation(AbstractTimeStamped):

    participants = models.ManyToManyField(
        "users.User", blank=True, related_name="conversations"
    )

    def __str__(self):
        participants = self.participants.all()
        username = []
        for paricipant in participants:
            username.append(paricipant.username)
        return ", ".join(username)

    def count_messages(self):
        return self.messages.count()

    count_messages.short_description = "Number of Messages"

    def count_participants(self):
        return self.participants.count()

    count_participants.short_description = "Number of Participants"


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
