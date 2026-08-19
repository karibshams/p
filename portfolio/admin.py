from django.contrib import admin
from .models import Feedback, ChatLog

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    ordering = ('-created_at',)

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'timestamp')
    ordering = ('-timestamp',)
