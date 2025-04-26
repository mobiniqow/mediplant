from django.contrib import admin

from ticket.models import Ticket, Message, TicketSection


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "section", "state", "created_at")
    search_fields = ("user__username", "section")
    list_filter = ("state",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "message_sender", "timestamp")
    search_fields = ("ticket__id", "message_sender__username")


@admin.register(TicketSection)
class TicketSection(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
