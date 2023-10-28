from django.contrib import admin
from .models import DoctorVisit, Prescription


@admin.register(DoctorVisit)
class DoctorVisitAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'state', 'patient', 'start_time', 'end_time']
    list_filter = ['state']
    search_fields = ['doctor__user__username', 'doctor__user__email', 'doctor__user__first_name',
                     'doctor__user__last_name', 'patient__user__username', 'patient__user__email',
                     'patient__user__first_name', 'patient__user__last_name']
    raw_id_fields = ['doctor', 'patient']
    readonly_fields = ['updated_at', 'created_at']


@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor_visit', 'description', 'therapy', 'created_at_format', 'updated_at']
    search_fields = ['doctor_visit__patient__first_name', 'doctor_visit__patient__last_name']
    list_filter = ['created_at']
    list_per_page = 20

    def created_at_format(self, obj):
        return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')

    created_at_format.short_description = 'تاریخ و زمان ایجاد'

    class Meta:
        model = Prescription
        verbose_name = 'نسخه بیمار'
        verbose_name_plural = 'نسخه‌های بیمار'