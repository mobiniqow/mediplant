from rest_framework import generics, status
from rest_framework.response import Response
from .models import DoctorVisit, DoctorVisitPrice, Prescription, PrescriptionSerializer
from .serializers import DoctorVisitSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class CreateDoctorVisitRequest(generics.CreateAPIView):
    queryset = DoctorVisit.objects.all()
    serializer_class = DoctorVisitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        patient = self.request.user.patientprofile
        serializer.save(patient=patient, state=DoctorVisit.State.REQUEST)


class CheckDoctorVisitStatus(generics.RetrieveAPIView):
    queryset = DoctorVisit.objects.all()
    serializer_class = DoctorVisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # فقط بیمار یا پزشک مربوطه می‌تواند وضعیت ویزیت را ببیند
        return DoctorVisit.objects.filter(patient=self.request.user.patientprofile)


class ListUserDoctorVisits(generics.ListAPIView):
    serializer_class = DoctorVisitSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # فیلتر کردن ویزیت‌ها برای کاربر وارد شده (پروفایل بیمار)
        return DoctorVisit.objects.filter(patient=self.request.user.patientprofile)


class CancelDoctorVisit(generics.UpdateAPIView):
    queryset = DoctorVisit.objects.all()
    serializer_class = DoctorVisitSerializer
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        visit = self.get_object()
        if visit.patient == self.request.user.patientprofile and visit.state == DoctorVisit.State.REQUEST:
            visit.state = DoctorVisit.State.FAILED  # لغو درخواست
            visit.save()
            return Response({"detail": "درخواست لغو شد"}, status=status.HTTP_200_OK)
        return Response({"detail": "اجازه لغو ندارید یا ویزیت قابل لغو نیست."}, status=status.HTTP_403_FORBIDDEN)


class FilterDoctorVisitsByState(generics.ListAPIView):
    queryset = DoctorVisit.objects.all()
    serializer_class = DoctorVisitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['state']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return DoctorVisit.objects.filter(patient=self.request.user.patientprofile)


class DoctorPrescriptionsListView(generics.ListAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        doctor = self.request.user.doctor  # فرض می‌کنیم که کاربر وارد شده پزشک است
        doctor_visits = DoctorVisit.objects.filter(doctor=doctor)
        return Prescription.objects.filter(doctor_visit__in=doctor_visits)


class PrescriptionDetailView(generics.RetrieveAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]


class AllPrescriptionsListView(generics.ListAPIView):
    queryset = Prescription.objects.all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]
