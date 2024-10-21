from django.urls import path
from .views import (
    CreateDoctorVisitRequest, CheckDoctorVisitStatus, ListUserDoctorVisits,
    CancelDoctorVisit, FilterDoctorVisitsByState, DoctorPrescriptionsListView, PrescriptionDetailView,
    AllPrescriptionsListView

)

urlpatterns = [
    path('doctor-visits/create/', CreateDoctorVisitRequest.as_view(), name='create-doctor-visit'),
    path('doctor-visits/<int:pk>/status/', CheckDoctorVisitStatus.as_view(), name='check-visit-status'),
    path('doctor-visits/user/', ListUserDoctorVisits.as_view(), name='list-user-visits'),
    path('doctor-visits/<int:pk>/cancel/', CancelDoctorVisit.as_view(), name='cancel-doctor-visit'),
    path('doctor-visits/filter/', FilterDoctorVisitsByState.as_view(), name='filter-doctor-visits'),
    path('prescriptions/doctor/', DoctorPrescriptionsListView.as_view(), name='doctor-prescriptions-list'),
    path('prescriptions/<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('prescriptions/all/', AllPrescriptionsListView.as_view(), name='all-prescriptions-list'),

]
