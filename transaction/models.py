from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid
import jdatetime
from sale.models import SaleBasket
import requests
import json

class DoctorTransaction(models.Model):
    class TransactionState(models.IntegerChoices):
        SUSPEND = 0, "در انتظار"
        REQUESTED = 1, "درخواست شده"
        ACCEPT = 2, "تأیید شده"
        FAILED = 3, "ناموفق"
        TIMEOUT = 4, "اتمام زمان"

    user = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.IntegerField(verbose_name="مبلغ")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    transaction_type = models.IntegerField(choices=TransactionState.choices, default=TransactionState.SUSPEND,
                                           verbose_name="وضعیت تراکنش")
    card = models.CharField("شماره کارت", max_length=33, null=True, blank=True)
    card_hash = models.CharField("هش کارت", max_length=128, null=True, blank=True)
    ref_id = models.CharField("کد پیگیری", max_length=32, null=True, blank=True)
    authority = models.CharField("Authority", max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "تراکنش پزشک"
        verbose_name_plural = "تراکنش‌های پزشکان"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'واریز'),
        ('withdrawal', 'برداشت'),
    ]

    TRANSACTION_STATUS = [
        ('success', 'موفق'),
        ('failed', 'ناموفق'),
        ('pending', 'در انتظار'),
        ('cancel', 'لغو شده'),
    ]

    class CourierType(models.IntegerChoices):
        POST = 1, 'پست'
        SNAPP = 2, 'اسنپ'

    courier_type = models.IntegerField(choices=CourierType.choices, default=CourierType.POST)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name="کاربر")
    amount = models.DecimalField(verbose_name="مبلغ", max_digits=10, decimal_places=2)
    transaction_type = models.CharField(verbose_name="نوع تراکنش", max_length=10, choices=TRANSACTION_TYPES)
    status = models.CharField(verbose_name="وضعیت", max_length=10, choices=TRANSACTION_STATUS, default='pending')
    timestamp = models.DateTimeField(verbose_name="تاریخ تراکنش", default=timezone.now)
    authority = models.CharField(verbose_name="Authority", max_length=100, null=True, blank=True)
    message = models.TextField(verbose_name="پیام", null=True, blank=True)
    address = models.TextField(verbose_name="آدرس", null=True, blank=True)
    lat = models.TextField(verbose_name="عرض جغرافیایی", null=True, blank=True)
    lng = models.TextField(verbose_name="طول جغرافیایی", null=True, blank=True)
    code_posti = models.CharField(verbose_name="کد پستی", max_length=40, default="")
    cart = models.ForeignKey(SaleBasket, on_delete=models.CASCADE, null=True, blank=True,
                             related_name='cart_transaction', verbose_name="سبد خرید")
    doctor_visit = models.ForeignKey('doctor_visit.DoctorVisit', on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name="visit", verbose_name="ویزیت پزشک")
    card = models.CharField(verbose_name="شماره کارت", max_length=33, null=True, blank=True)
    card_hash = models.CharField(verbose_name="هش کارت", max_length=128, null=True, blank=True)
    ref_id = models.CharField(verbose_name="کد پیگیری", max_length=32, null=True, blank=True)

    class Meta:
        verbose_name = "تراکنش"
        verbose_name_plural = "تراکنش‌ها"

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} - {self.status}"

    def get_shamsi_date(self):
        return jdatetime.datetime.fromgregorian(datetime=self.timestamp).strftime('%Y/%m/%d')

    def get_transaction_details(self):
        return {
            'amount': self.amount,
            'card_number': self.card,
            'date_shamsi': self.get_shamsi_date(),
        }


class Payment(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, verbose_name="کاربر")
    cart = models.ForeignKey(SaleBasket, on_delete=models.CASCADE, verbose_name="سبد خرید")
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE, verbose_name="تراکنش مرتبط")
    payment_url = models.URLField(verbose_name="آدرس پرداخت", null=True, blank=True)
    status = models.CharField(verbose_name="وضعیت پرداخت", max_length=10, choices=[
        ('pending', 'در انتظار'),
        ('completed', 'تکمیل شده'),
        ('failed', 'ناموفق')
    ], default='pending')
    created_at = models.DateTimeField(verbose_name="تاریخ ایجاد", auto_now_add=True)

    class Meta:
        verbose_name = "پرداخت"
        verbose_name_plural = "پرداخت‌ها"

    def __str__(self):
        return f"پرداخت {self.cart.user.user_name} - {self.status}"

    def initiate_payment(self):
        amount = self.cart.price
        if amount <= 0:
            raise ValueError("سبد خرید خالی است یا مبلغ پرداخت صحیح نیست.")

        url = "https://api.zarinpal.com/pg/v4/payment/request.json"
        data = {
            'merchant_id': settings.MERCHANT_ID,
            'amount': str(amount),
            'callback_url': settings.CALLBACK_URL,
            'description': f"پرداخت برای سبد خرید {self.user.user_name}",
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            response_data = json.loads(response.text)
            if response_data['data']['code'] == 100:
                self.payment_url = response_data['data']
                transaction = self.transaction
                transaction.authority = response_data['data']['authority']
                transaction.save()
                self.status = 'pending'
                self.save()
                return self.payment_url
            else:
                self.status = 'failed'
                self.save()
                raise Exception(f"خطا در درخواست پرداخت: {response_data['data']['message']}")
        else:
            self.status = 'failed'
            self.save()
            raise Exception("خطا در ارتباط با زرین‌پال")