from django.contrib import admin
from .models import Feedback, ChatLog, VisitorCount

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    ordering = ('-created_at',)

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user_message', 'timestamp')
    ordering = ('-timestamp',)

@admin.register(VisitorCount)
class VisitorAdmin(admin.ModelAdmin):
    list_display = ('date', 'count')
    ordering = ('-date',)