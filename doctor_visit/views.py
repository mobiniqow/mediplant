from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor.models import Doctor
from doctor_visit.models import DoctorVisit, DoctorVisitChat
from doctor_visit.serializers import DoctorVisitChatSerializer, UserChatRequest
from transaction.models import Transaction, DoctorTransaction


# authority = models.CharField(max_length=100, null=True, blank=True)
# message = models.TextField(null=True, blank=True)
# address = models.TextField(null=True, blank=True)
# lat = models.TextField(null=True, blank=True)
# lng = models.TextField(null=True, blank=True)
# code_posti = models.CharField(max_length=40, default="")
# cart = models.ForeignKey(SaleBasket, on_delete=models.CASCADE, null=True, blank=True, related_name='cart_transaction')
# card = models.CharField(max_length=33, null=True, blank=True)
# card_hash = models.CharField(max_length=128, null=True, blank=True)
# ref_id = models.CharField(max_length=32, null=True, blank=True)

class RequestToDoctor(APIView):
    def post(self, request, doctor_id, **kwargs):
        doctor = get_object_or_404(Doctor, pk=doctor_id)
        user = request.user
        if DoctorVisit.objects.filter(
                doctor=doctor,
                user=user,
                state=DoctorVisit.State.ACCEPT
        ):
            return Response(status=204)

        transaction, _ = DoctorTransaction.objects.get_or_create(
            user=user, amount=1100,
            transaction_type=DoctorTransaction.TransactionState.SUSPEND,
        )

        DoctorVisit.objects.get_or_create(
            doctor=doctor,
            user=user,
        )

        return Response({"transaction_id": transaction.id}, status=200)


class DoctorVisitChatListView(generics.ListAPIView):
    serializer_class = DoctorVisitChatSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor_visit_id = self.kwargs['doctor_visit_id']
        return DoctorVisitChat.objects.filter(doctor_id=doctor_visit_id)


class UserSendToDoctorMessage(APIView):
    def post(self, request, doctor_visit_id, **kwargs):
        visit = get_object_or_404(DoctorVisit, pk=doctor_visit_id, state=DoctorVisit.State.ACCEPT)
        data = request.data.copy()
        chat = UserChatRequest(data=data, context={'doctor_id': doctor_visit_id, 'is_doctor': False})

        if chat.is_valid(raise_exception=True):
            chat_instance = chat.save()
            chat_message = DoctorVisitChat.objects.create(
                doctor_id=doctor_visit_id,
                content=data['content'],
                is_doctor=False,
                media=data.get('media'),
            )

            result = DoctorVisitChatSerializer(chat_message)
            return Response(result.data, status=201)


class UserFinishChat(APIView):
    def post(self, request, doctor_visit_id, **kwargs):
        visit: DoctorVisit = get_object_or_404(DoctorVisit, pk=doctor_visit_id, state=DoctorVisit.State.ACCEPT)
        visit.state = DoctorVisit.State.UserEND
        visit.save()
        return Response(status=204)
