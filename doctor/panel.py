from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics, permissions
from django.utils.timezone import now
from jdatetime import timedelta
from doctor.models import Doctor, DoctorSettlement
from doctor.serializer import DoctorLoginSerializer, DoctorSettlementSerializer, DoctorShopProfileUpdateSerializer
from doctor_visit.models import DoctorVisit, Prescription
from doctor_visit.serializers import DoctorVisitSerializer, PrescriptionSerializer
from shop.serializers import UserShopProfileUpdateSerializer
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer


class DoctorLoginView(APIView):
    def post(self, request):
        serializer = DoctorLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorVisitListView(APIView):
    def get(self, request):
        visits = DoctorVisit.objects.filter(doctor__user=request.user).exclude(state=DoctorVisit.State.REQUEST).exclude(
            state=DoctorVisit.State.FAILED)
        serializers = DoctorVisitSerializer(
            visits,
            many=True
        )
        return Response(
            data=serializers.data,
            status=status.HTTP_200_OK
        )


class NewDoctorVisitListView(APIView):
    def get(self, request):
        visits = DoctorVisit.objects.filter(doctor__user=request.user, state=DoctorVisit.State.REQUEST)
        serializers = DoctorVisitSerializer(
            visits,
            many=True
        )
        return Response(
            data=serializers.data,
            status=status.HTTP_200_OK
        )

    def post(self, request, request_id):
        try:
            visit = DoctorVisit.objects.get(id=request_id, doctor__user=request.user, state=DoctorVisit.State.REQUEST)
            visit.state = DoctorVisit.State.ACCEPT  # تغییر وضعیت به FAILED به معنی حذف درخواست
            visit.save()
            return Response(
                {"message": "درخواست ویزیت با موفقیت حذف شد."},
                status=status.HTTP_204_NO_CONTENT
            )
        except DoctorVisit.DoesNotExist:
            return Response(
                {"error": "درخواست ویزیت پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )


    def delete(self, request, request_id):
        try:
            visit = DoctorVisit.objects.get(id=request_id, doctor__user=request.user, state=DoctorVisit.State.REQUEST)
            visit.state = DoctorVisit.State.FAILED  # تغییر وضعیت به FAILED به معنی حذف درخواست
            visit.save()
            return Response(
                {"message": "درخواست ویزیت با موفقیت حذف شد."},
                status=status.HTTP_204_NO_CONTENT
            )
        except DoctorVisit.DoesNotExist:
            return Response(
                {"error": "درخواست ویزیت پیدا نشد."},
                status=status.HTTP_404_NOT_FOUND
            )


class DoctorTransactionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        return Transaction.objects.filter(doctor_visit__doctor=doctor)


class DoctorSettlementRequestAPIView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSettlementSerializer

    def get_queryset(self):
        doctor = get_object_or_404(Doctor, user=self.request.user)
        return DoctorSettlement.objects.filter(doctor=doctor)



class DoctorDetailView(APIView):
    """API برای دریافت و به‌روزرسانی اطلاعات فروشگاه"""
    permission_classes = [permissions.IsAuthenticated,  ]

    def get(self, request):
        """دریافت اطلاعات فروشگاه کاربر"""
        doctor = get_object_or_404(Doctor, user=request.user)
        serializer = DoctorShopProfileUpdateSerializer(doctor)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """به‌روزرسانی اطلاعات فروشگاه"""
        doctor = get_object_or_404(Doctor, user=request.user)
        serializer = DoctorShopProfileUpdateSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorEarningsStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor_visits = DoctorVisit.objects.filter(doctor__user=request.user)  # دریافت ویزیت‌های مربوط به پزشک
        filter_type = request.query_params.get("filter", "daily")  # مقدار پیش‌فرض: روزانه

        today = now().date()
        periods = []

        for i in range(7):  # محاسبه برای ۷ دوره‌ی قبلی
            if filter_type == "daily":
                start_date = today - timedelta(days=(i + 1))
                end_date = today - timedelta(days=i)
            elif filter_type == "weekly":
                start_date = today - timedelta(weeks=(i + 1))
                end_date = today - timedelta(weeks=i)
            elif filter_type == "monthly":
                start_date = today - timedelta(weeks=(i + 1) * 4)  # ۴ هفته تقریباً برابر با یک ماه
                end_date = today - timedelta(weeks=i * 4)
            else:
                return Response({"error": "نوع فیلتر معتبر نیست. از daily, weekly یا monthly استفاده کنید."}, status=400)

            transactions = Transaction.objects.filter(
                doctor_visit__in=doctor_visits,
                timestamp__date__gte=start_date,
                timestamp__date__lt=end_date,
                status="success"  # فقط تراکنش‌های موفق
            )

            total_transactions = transactions.count()
            total_income = sum(transaction.amount for transaction in transactions)

            periods.append({
                "start_date": start_date,
                "end_date": end_date - timedelta(days=1),  # نمایش تا روز قبل از `end_date`
                "total_transactions": total_transactions,
                "total_income": total_income,
            })

        return Response({
            "filter": filter_type,
            "data": periods
        })


class PrescriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, visit_id):
        """لیست نسخه‌های پزشک برای یک ویزیت خاص"""
        visit = get_object_or_404(DoctorVisit, id=visit_id, doctor=request.user)
        prescriptions = Prescription.objects.filter(doctor_visit=visit)

        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, visit_id):
        """ایجاد یک نسخه برای ویزیت خاص"""
        visit = get_object_or_404(DoctorVisit, id=visit_id, doctor=request.user)

        serializer = PrescriptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(doctor_visit=visit)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, visit_id):
        """ویرایش یک نسخه بر اساس ویزیت"""
        visit = get_object_or_404(DoctorVisit, id=visit_id, doctor=request.user)
        prescription = get_object_or_404(Prescription, doctor_visit=visit)

        serializer = PrescriptionSerializer(prescription, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)