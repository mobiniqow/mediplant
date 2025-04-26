from django.contrib import admin
from .models import ShopReport, DoctorReport, UserReport


@admin.register(ShopReport)
class ShopReportAdmin(admin.ModelAdmin):
    list_display = ['shop', 'user', 'message']
    list_filter = ['shop', 'user']

    class Meta:
        model = ShopReport


@admin.register(DoctorReport)
class DoctorReportAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'user', 'message']
    list_filter = ['doctor', 'user']

    class Meta:
        model = DoctorReport


@admin.register(UserReport)
class UserReportAdmin(admin.ModelAdmin):
    list_display = ['reported_user', 'plaintiff', 'message']
    list_filter = ['reported_user', 'plaintiff']

    class Meta:
        model = UserReport