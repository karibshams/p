from django.db import models

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name} — {self.created_at.strftime('%Y-%m-%d')}"

class ChatLog(models.Model):
    user_message = models.TextField()
    ai_reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Chat @ {self.timestamp.strftime('%Y-%m-%d %H:%M')}"
