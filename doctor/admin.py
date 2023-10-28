from django.contrib import admin
from .models import DockterBranch, History, Doctor, DocktorPhone, DoctorHistory, DoctorVisitPrice, PatientProfile


class DoctorHistoryInline(admin.TabularInline):
    model = DoctorHistory


class DoctorVisitPriceInline(admin.TabularInline):
    model = DoctorVisitPrice


class DocktorPhoneInline(admin.TabularInline):
    model = DocktorPhone


class PatientProfileInline(admin.TabularInline):
    model = PatientProfile


@admin.register(DockterBranch)
class DockterBranchAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['history']
    search_fields = ['history']


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'branch', 'state', 'id_active']
    list_filter = ['state', 'id_active']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user', 'branch']
    readonly_fields = ['register_time']
    inlines = [DoctorHistoryInline, DoctorVisitPriceInline, DocktorPhoneInline, PatientProfileInline]


@admin.register(DocktorPhone)
class DocktorPhoneAdmin(admin.ModelAdmin):
    list_display = ['phone', 'doctor']
    search_fields = ['phone']
    raw_id_fields = ['doctor']


@admin.register(DoctorHistory)
class DoctorHistoryAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'history']
    raw_id_fields = ['doctor', 'history']


@admin.register(DoctorVisitPrice)
class DoctorVisitPriceAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'price', 'timing', 'state']
    list_filter = ['state']
    raw_id_fields = ['doctor']


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'doctor']
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name']
    raw_id_fields = ['user', 'doctor']