import django_filters

from doctor.models import Doctor

class DoctorFilter(django_filters.FilterSet):
    branch = django_filters.BaseInFilter(field_name="branch", lookup_expr="in")

    class Meta:
        model = Doctor
        fields = ['branch', 'state', 'responsiveness', 'id_active']