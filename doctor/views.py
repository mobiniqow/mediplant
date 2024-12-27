from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer
from .filters import DoctorFilter
from rest_framework import generics
from .models import DockterBranch
from .serializers import DockterBranchSerializer


class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DoctorFilter


class DockterBranchListView(generics.ListAPIView):
    queryset = DockterBranch.objects.all()
    serializer_class = DockterBranchSerializer
