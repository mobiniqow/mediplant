import django_filters
from .models import DoctorVisit

class DoctorVisitFilter(django_filters.FilterSet):
    class Meta:
        model = DoctorVisit
        fields = ['state']  # فیلتر بر اساس وضعیت
