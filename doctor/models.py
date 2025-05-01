from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from ckeditor.fields import RichTextField
from account.models import User


class DockterBranch(models.Model):
    name = models.CharField(max_length=33, unique=True, verbose_name='نام')

    class Meta:
        verbose_name = "شاخه پزشکی"
        verbose_name_plural = "شاخه‌های پزشکی"


class History(models.Model):
    history = models.TextField(max_length=33, verbose_name='تاریخچه')

    class Meta:
        verbose_name = "تاریخچه"
        verbose_name_plural = "تاریخچه‌ها"


class Doctor(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        DE_ACTIVE = 2
        REPORTED = 3
        BANNED = 4

    class Responsiveness(models.IntegerChoices):
        DARK = 0
        WHITE = 1
        SILVER = 2
        GOLD = 3

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    national_code = models.CharField(max_length=10, blank=True, null=True, verbose_name='کد ملی', )
    public_phone = models.CharField(max_length=12, verbose_name='شماره تلفن', blank=True, null=True)
    branch = models.ForeignKey(DockterBranch, on_delete=models.SET_NULL, null=True, verbose_name='شاخه تحصیلی')
    address = models.TextField(verbose_name='آدرس')
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت')
    certificate = models.FileField(upload_to='doctor/certificate',
                                   validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], blank=True, null=True,
                                   verbose_name='تصویر جواز')
    picture = models.FileField(upload_to='doctor/avatar',
                               validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])], blank=True,
                               verbose_name='تصویر پرسنلی')
    description = RichTextField(verbose_name='توضیحات', default=None)
    id_active = models.BooleanField(verbose_name='وضعیت فعالیت')
    register_time = models.IntegerField(verbose_name='مهلت ثبت نام', default=0)
    responsiveness = models.IntegerField(choices=Responsiveness.choices, default=Responsiveness.WHITE,
                                         verbose_name='نوع عملکرد')
    postal_code = models.CharField(max_length=12, verbose_name='کد پستی')
    shaba = models.CharField(max_length=12, verbose_name='شماره شبا')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    medical_system_code = models.CharField(max_length=10, default="2112032")
    instagram = models.CharField(max_length=100, blank=True, null=True, verbose_name='اینستاگرام')
    whatsapp = models.CharField(max_length=100, blank=True, null=True, verbose_name='whatsapp')
    start_time = models.IntegerField(validators=(MinValueValidator(1), MaxValueValidator(24)), default=0,
                                     verbose_name='زمان شروع')
    end_time = models.IntegerField(validators=(MinValueValidator(1), MaxValueValidator(24)), default=0,
                                   verbose_name='زمان پایان')

    class Meta:
        verbose_name = "پزشک"
        verbose_name_plural = "پزشکان"


class DocktorPhone(models.Model):
    phone = models.CharField(max_length=12, verbose_name="شماره تلفن")
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, verbose_name='پزشک')

    class Meta:
        verbose_name = "شماره تلفن پزشک"
        verbose_name_plural = "شماره تلفن‌های پزشک"


class DoctorHistory(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='پزشک')
    history = models.ForeignKey(History, on_delete=models.CASCADE, verbose_name='تاریخچه')

    class Meta:
        verbose_name = "تاریخچه دکتر"
        verbose_name_plural = "تاریخچه‌های دکتر"


class DoctorVisitPrice(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        DE_ACTIVE = 2

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='پزشک')
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='قیمت')
    timing = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='زمان')
    state = models.IntegerField(choices=State.choices, verbose_name='وضعیت')

    class Meta:
        verbose_name = "قیمت و زمان ویزیت دکتر"
        verbose_name_plural = "قیمت و زمان ویزیت‌های دکتر"


class PatientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name='پزشک')

    class Meta:
        verbose_name = "پروفایل بیمار"
        verbose_name_plural = "پروفایل بیماران"


class DoctorSettlement(models.Model):
    class STATUS(models.IntegerChoices):
        PENDING = 0, "در انتظار بررسی"
        APPROVED = 1, "تایید شده"
        REJECTED = 2, "رد شده"
        PAID = 3, "پرداخت شده"

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, verbose_name="فروشگاه")
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="مبلغ درخواستی")
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.PENDING,
                                 verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درخواست")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر وضعیت")
    receipt_image = models.ImageField(upload_to="settlements/receipts/", null=True, blank=True,
                                      verbose_name="تصویر فیش پرداختی")
    transaction_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="شناسه تراکنش")

    def __str__(self):
        return f"تسویه حساب {self.doctor.user.user_name} - {self.amount} تومان - {self.get_status_display()}"
