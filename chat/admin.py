from django.contrib import admin
from .models import ChatSession, Message


@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'content_object']
    readonly_fields = ['created_at']

    class Meta:
        model = ChatSession


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['session', 'sender', 'content', 'created_at']
    readonly_fields = ['created_at']

    class Meta:
        model = Message
