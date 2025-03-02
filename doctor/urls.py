from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, DoctorBranchList

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet, basename='doctor')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/branch', DoctorBranchList.as_view(), name='branch-list')
]
