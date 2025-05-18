from django.contrib import admin
from .models import TicketSection, Ticket, Message


@admin.register(TicketSection)
class TicketSectionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)
    verbose_name = "بخش تیکت"
    verbose_name_plural = "بخش‌های تیکت"


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "state", "created_at")
    list_filter = ("state", "created_at", "section")
    search_fields = ("title", "description", "user__username")
    autocomplete_fields = ("user", "assigned_to_store", "assigned_to_doctor", "section")
    readonly_fields = ("created_at",)
    fieldsets = (
        (None, {
            "fields": ("title", "description", "state")
        }),
        ("کاربر و مسئولین", {
            "fields": ("user", "assigned_to_store", "assigned_to_doctor")
        }),
        ("اطلاعات دیگر", {
            "fields": ("section", "created_at")
        }),
    )
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'assigned_to_store', 'assigned_to_doctor', 'section')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "message_sender", "is_user", "timestamp")
    list_filter = ("is_user", "timestamp")
    search_fields = ("text", "message_sender__username", "ticket__id")
    autocomplete_fields = ("ticket", "message_sender")
    readonly_fields = ("timestamp",)
    fieldsets = (
        (None, {
            "fields": ("ticket", "message_sender", "is_user")
        }),
        ("محتوا", {
            "fields": ("text", "file")
        }),
        ("زمان", {
            "fields": ("timestamp",)
        }),
    )
