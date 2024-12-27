from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from doctor.models import PatientProfile, DoctorVisitPrice
from sickness.models import TraditionalMedicineDisease
from transaction.models import Transaction


class DoctorVisit(models.Model):
    class State(models.IntegerChoices):
        REQUEST = 0
        ACCEPT = 1
        FAILED = 2
        END = 3
        REPORT = 4

    doctor = models.ForeignKey(DoctorVisitPrice, on_delete=models.CASCADE, null=True, verbose_name='پزشک')
    state = models.IntegerField(choices=State.choices, default=State.REQUEST, verbose_name='وضعیت')
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, null=True, verbose_name='بیمار')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    start_time = models.DateTimeField(verbose_name='زمان شروع')
    end_time = models.DateTimeField(verbose_name='زمان پایان')
    user_rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                    verbose_name='امتیاز کاربر')
    doctor_rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                      verbose_name='امتیاز پزشک')
    time = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='زمان')
    comment = models.TextField(verbose_name='نظر')
    transaction = models.ForeignKey(Transaction, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "ویزیت دکتر"
        verbose_name_plural = "ویزیت‌های دکتر"


class Prescription(models.Model):
    doctor_visit = models.ForeignKey(DoctorVisit, on_delete=models.SET_NULL, null=True)
    traditional_medicine_disease = models.ForeignKey(TraditionalMedicineDisease, on_delete=models.SET_NULL, null=True,
                                                     verbose_name='بیمار')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    description = models.TextField(verbose_name='توضیحات')
    therapy = models.TextField(verbose_name='دارو و درمان')

    class Meta:
        verbose_name = "نسخه بیمار"
        verbose_name_plural = "نسخه های بیمار"
