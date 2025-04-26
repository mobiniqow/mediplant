from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class TicketState(models.IntegerChoices):
    OPEN = 1, "Open"
    IN_PROGRESS = 2, "In Progress"
    CLOSED = 3, "Closed"


class TicketSection(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    section = models.ForeignKey(TicketSection, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets")
    assigned_to_store = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                          related_name="store_tickets")
    assigned_to_doctor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                           related_name="doctor_tickets")
    # status = models.IntegerField(choices=TicketState.choices, default=TicketState.OPEN)
    type_state = models.IntegerField(choices=TicketState.choices, default=TicketState.OPEN,null=True, blank=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ticket {self.id} - {self.user.username}"


class Message(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    message_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_message')
    is_user = models.BooleanField(default=True)
    text = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="ticket_files/", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in Ticket {self.ticket.id}"
