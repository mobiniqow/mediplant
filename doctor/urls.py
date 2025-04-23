from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .panel import DoctorLoginView, DoctorVisitListView, NewDoctorVisitListView, DoctorTransactionsAPIView, \
    DoctorSettlementRequestAPIView, DoctorDetailView, DoctorEarningsStatisticsAPIView, PrescriptionAPIView
from .views import DoctorViewSet, DoctorBranchList

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/branch', DoctorBranchList.as_view(), name='branch-list'),
    # doctor api list
    path('login/', DoctorLoginView.as_view(), name='doctor-login'),
    path('visit-list/', DoctorVisitListView.as_view(), name='doctor-visit-list'),
    path('new-visit/', NewDoctorVisitListView.as_view(), name='doctor-visit-list'),
    path('new-visit/<int:request_id>/', NewDoctorVisitListView.as_view(), name='doctor-request'),  # for browsable API
    path('transaction', DoctorTransactionsAPIView.as_view(), name='doctor-transaction'),  # for browsable API
    path('settlements/', DoctorSettlementRequestAPIView.as_view(), name='doctor-settlement'),
    path('profile/', DoctorDetailView.as_view(), name='doctor_detail'),
    path('sales-stats/', DoctorEarningsStatisticsAPIView.as_view(), name='doctor-sales-stats'),
    path('prescriptions/<int:visit_id>/', PrescriptionAPIView.as_view(), name='prescription-detail'),
]
