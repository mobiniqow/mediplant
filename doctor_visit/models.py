from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.db import models
from pygments.lexer import default

from account.models import User
from doctor.models import PatientProfile, DoctorVisitPrice, Doctor
from sickness.models import TraditionalMedicineDisease
from transaction.models import Transaction, DoctorTransaction


class DoctorVisit(models.Model):
    class State(models.IntegerChoices):
        REQUEST = 0
        ACCEPT = 1
        FAILED = 2
        UserEND = 3
        DoctorEnd = 4
        REPORT = 5

    # doctor = models.ForeignKey(DoctorVisitPrice, on_delete=models.CASCADE, null=True, verbose_name='پزشک')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, verbose_name='پزشک')
    state = models.IntegerField(choices=State.choices, default=State.REQUEST, verbose_name='وضعیت')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='بیمار')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ به‌روزرسانی')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    start_time = models.DateTimeField(verbose_name='زمان شروع', null=True, blank=True)
    end_time = models.DateTimeField(verbose_name='زمان پایان', null=True, blank=True)
    user_rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                    verbose_name='امتیاز کاربر', null=True, blank=True)
    doctor_rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],
                                      verbose_name='امتیاز پزشک', null=True, blank=True)
    time = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='زمان')
    comment = models.TextField(verbose_name='نظر', null=True, blank=True)
    transaction = models.ForeignKey(DoctorTransaction, on_delete=models.SET_NULL, null=True)

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


class DoctorVisitChat(models.Model):
    doctor = models.ForeignKey(DoctorVisit, on_delete=models.CASCADE, null=True, blank=True)
    is_doctor = models.BooleanField(default=True)
    content = models.TextField(null=True, blank=True)
    media = models.FileField(validators=[FileExtensionValidator(['png', 'jpeg', 'jpg', 'mp3', 'wav'])], null=True,
                             blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(default=datetime.now, blank=True)
    is_read = models.BooleanField(default=False)
