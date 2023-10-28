from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models 

from doctor_visit.models import DoctorVisit
from sale.models import SaleBasket


class FeedBackShop(models.Model):

    class State(models.IntegerChoices):
        SUSPEND = 0, 'تعلیق شده'
        ACCEPT = 1, 'تایید شده'
        FAILED = 2, 'ناموفق'
        REPORT = 3, 'گزارش شده'

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت')
    shop = models.ForeignKey(SaleBasket, on_delete=models.CASCADE, verbose_name='سبد خرید')
    comment = models.TextField(verbose_name='نظر')
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='امتیاز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'بازخورد فروشگاه'
        verbose_name_plural = 'بازخوردهای فروشگاه'


class FeedBackDoctorVisit(models.Model):

    class State(models.IntegerChoices):
        SUSPEND = 0, 'تعلیق شده'
        ACCEPT = 1, 'تایید شده'
        FAILED = 2, 'ناموفق'
        REPORT = 3, 'گزارش شده'

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت')
    visit = models.ForeignKey(DoctorVisit, on_delete=models.CASCADE, verbose_name='ویزیت')
    comment = models.TextField(verbose_name='نظر')
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='امتیاز')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'بازخورد ویزیت'
        verbose_name_plural = 'بازخوردهای ویزیت ها'
