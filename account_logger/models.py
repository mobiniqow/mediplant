from django.db import models
from django.db.models import SET_NULL
from django_jalali.db import models as jmodels

from account.models import User


class UserRefLogs(models.Model):
    ref = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name="user_referenced",
                            verbose_name='معرفی شده توسط کاربر')
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, related_name="new_user",
                             verbose_name='کاربر جدید')
    created_at = jmodels.jDateField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'لاگ معرفی کاربر'
        verbose_name_plural = 'لاگ‌های معرفی کاربران'


class UserActivateLogs(models.Model):
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name='کاربر')
    created_at = jmodels.jDateField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'لاگ فعال‌سازی کاربر'
        verbose_name_plural = 'لاگ‌های فعال‌سازی کاربران'

# todo farsish konam badan
