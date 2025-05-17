from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketState(models.IntegerChoices):
    OPEN = 1, "باز"
    IN_PROGRESS = 2, "در حال بررسی"
    CLOSED = 3, "بسته شده"


class TicketSection(models.Model):
    name = models.CharField("نام بخش", max_length=100, unique=True)

    class Meta:
        verbose_name = "بخش تیکت"
        verbose_name_plural = "بخش‌های تیکت"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets", verbose_name="کاربر ثبت‌کننده")
    section = models.ForeignKey(
        TicketSection, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets", verbose_name="بخش"
    )
    assigned_to_store = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="store_tickets", verbose_name="واگذار شده به فروشگاه"
    )
    assigned_to_doctor = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL,
        related_name="doctor_tickets", verbose_name="واگذار شده به پزشک"
    )
    description = models.TextField("توضیحات", null=True, blank=True)
    state = models.IntegerField("وضعیت", choices=TicketState.choices, default=TicketState.OPEN, null=True, blank=True)
    title = models.CharField("عنوان", max_length=100)
    created_at = models.DateTimeField("تاریخ ثبت", auto_now_add=True)

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت‌ها"

    def __str__(self):
        return f"تیکت {self.id} - {self.user.username}"


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages", verbose_name="تیکت")
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_message', verbose_name="فرستنده")
    is_user = models.BooleanField("ارسال توسط کاربر", default=True)
    text = models.TextField("متن پیام", null=True, blank=True)
    file = models.FileField("فایل پیوست", upload_to="ticket_files/", null=True, blank=True)
    timestamp = models.DateTimeField("تاریخ ارسال", auto_now_add=True)

    class Meta:
        verbose_name = "پیام"
        verbose_name_plural = "پیام‌ها"

    def __str__(self):
        return f"پیام {self.id} در تیکت {self.ticket.id}"
