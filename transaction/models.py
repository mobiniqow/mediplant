from django.core.validators import MinValueValidator
from django.db import models
from account.models import User


class Transaction(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        PAYMENT_GATEWAY = 1
        FAILED = 2
        SUCCESSFUL = 3
        REPORTED = 4

    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='مبلغ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت')
    transaction_number = models.CharField(max_length=20, verbose_name='شماره تراکنش')
    payment_gateway = models.CharField(max_length=50, verbose_name='نام درگاه پرداخت')
    description = models.TextField(blank=True, verbose_name='توضیحات')

    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'
