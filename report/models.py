from django.db import models

from account.models import User
from doctor.models import Doctor


class ShopReport(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        IN_PROCESS = 1
        PASSED = 2
        FAILED = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    shop = models.ForeignKey('shop.Shop', on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه',
                             related_name='shop_report')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    message = models.TextField(verbose_name='پیام')

    class Meta:
        verbose_name = 'گزارش فروشگاه'
        verbose_name_plural = 'گزارش‌های فروشگاه'


class DoctorReport(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        IN_PROCESS = 1
        PASSED = 2
        FAILED = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name='دکتر')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    message = models.TextField(verbose_name='پیام')

    class Meta:
        verbose_name = 'گزارش دکتر'
        verbose_name_plural = 'گزارش‌های دکتر'


class UserReport(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        IN_PROCESS = 1
        PASSED = 2
        FAILED = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    reported_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_user',
                                      verbose_name='کاربر گزارش شده')
    plaintiff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='plaintiff_user',
                                  verbose_name='کاربر خواهان')
    message = models.TextField(verbose_name='پیام')

    class Meta:
        verbose_name = 'گزارش کاربر'
        verbose_name_plural = 'گزارش‌های کاربران'
