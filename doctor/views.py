from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend

from encyclopedia.views import CustomPagination
from .filters.DoctorFilter import DoctorFilter
from .models import Doctor, DockterBranch
from .serializer import DoctorSerializer,DockterBranchSerializer


class DoctorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_class = DoctorFilter
    search_fields = ['user__username', 'address', 'description']
    ordering_fields = ['register_time', 'state']
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = super().get_queryset()
        branches = self.request.query_params.getlist('branch')

        if branches:
            try:
                branch_ids = [int(branch) for branch in branches]
                queryset = queryset.filter(branch__id__in=branch_ids)
            except ValueError:
                pass

        return queryset


class DoctorBranchList(generics.ListAPIView):
    queryset = DockterBranch.objects.all()
    serializer_class = DockterBranchSerializer
