from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Ticket, Message, TicketSection, TicketState
from .serializers import TicketSerializer, MessageSerializer, TicketSectionSerializer


# ✅ ایجاد و لیست کردن تیکت‌ها
class TicketListCreateView(generics.CreateAPIView, generics.ListAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ✅ نمایش جزئیات یک تیکت خاص و تغییر وضعیت آن
class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TicketSerializer

    def get_queryset(self):
        return Ticket.objects.all().order_by('-created_at')


# ✅ ارسال پیام جدید در یک تیکت خاص
class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        ticket_id = self.kwargs['ticket_id']
        ticket = get_object_or_404(Ticket, id=ticket_id)
        serializer.save(ticket=ticket, sender=self.request.user)


# ✅ اختصاص دادن تیکت به یک پزشک یا فروشنده توسط ادمین
class TicketAssignView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, pk):
        ticket = get_object_or_404(Ticket, id=pk)
        assignee_id = request.data.get('assignee_id')

        if not assignee_id:
            return Response({"error": "assignee_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        ticket.assigned_to_id = assignee_id
        ticket.status = TicketState.IN_PROGRESS
        ticket.save()

        return Response({"message": "Ticket assigned successfully"}, status=status.HTTP_200_OK)


# ✅ دریافت لیست تیکت‌های کاربر (فروشنده/پزشک)
class UserTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(assigned_to=self.request.user)


# ✅ دریافت لیست همه تیکت‌ها برای ادمین
class AdminTicketListView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Ticket.objects.all()


class TicketSectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketSection.objects.all()
    serializer_class = TicketSectionSerializer
