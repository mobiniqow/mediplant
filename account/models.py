import re
import string
import random

from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import SET_NULL

from city.models import City, CityLocation


def phone_validator(v):
    pattern = r"^09[0|1|2|3][0-9]{8}$"
    if not re.match(pattern, v):
        raise ValidationError("invalid phone number")


class BasicUserManager(BaseUserManager):
    def create_user(self, phone, password=None):
        if not phone:
            raise ValueError("Users must enter a phone")

        user = self.model(phone=phone)
        user.state = User.State.SUSPEND
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None):
        user = self.model(phone=phone)
        user.is_staff = True
        user.set_password(password)
        user.state = User.State.ACTIVE
        user.save()
        return user

    def create_guest_user(self):
        guest = GuestCounter.objects.create()
        phone = self.generate_17_digit_number(guest.id)
        user = self.model(phone=phone)
        user.state = User.State.GUEST
        user.save()
        return user

    def generate_17_digit_number(self,input_number):
        # تبدیل عدد ورودی به رشته
        input_str = str(input_number)

        # محاسبه تعداد صفرهای مورد نیاز برای پر کردن
        remaining_length = 17 - len(input_str) - 3  # 3 رقم برای 123 در ابتدا

        # بررسی اینکه طول عدد ورودی بیشتر از 14 رقم نباشد
        if remaining_length < 0:
            raise ValueError("عدد ورودی نباید بیشتر از 14 رقم باشد.")

        # ایجاد عدد 17 رقمی که با 123 شروع می‌شود و باقی با صفر پر می‌شود
        result = "123" + "0" * remaining_length + input_str

        return result


class User(AbstractBaseUser, PermissionsMixin):
    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        REPORTED = 2
        BANNED = 3
        GUEST = 4

    class UserActivationState(models.IntegerChoices):
        WHITE = 0
        SILVER = 1
        GOLD = 2

    class Gender(models.IntegerChoices):
        MAN = 1, 'مرد'
        WOMAN = 0, 'زن'

    avatar = models.FileField(upload_to='paccount/user/avatar',
                              validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], blank=True,
                              verbose_name='تصویر')
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت')
    gender = models.IntegerField(choices=Gender.choices, default=Gender.MAN, verbose_name=' ')
    activation_state = models.IntegerField(choices=UserActivationState.choices, default=UserActivationState.WHITE,
                                           verbose_name='نوع پلن')
    user_name = models.CharField(max_length=83, verbose_name='نام و نام خانوادگی', blank=True)
    phone = models.CharField(max_length=17, unique=True, validators=[phone_validator], verbose_name='شماره تلفن')
    objects = BasicUserManager()
    USERNAME_FIELD = "phone"
    phone_otp = models.CharField(max_length=6, blank=True, null=True, verbose_name="OTP for phone verification")
    email_otp = models.CharField(max_length=6, blank=True, null=True, verbose_name="OTP for email verification")
    phone_otp_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Time when phone OTP was sent")
    email_otp_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Time when email OTP was sent")

    is_staff = models.BooleanField(default=False)
    email = models.EmailField(verbose_name='ایمیل', blank=True)
    referral_code = models.CharField(max_length=8, unique=True, editable=False)
    city = models.CharField(max_length=100, null=True, verbose_name='شهر', blank=True)
    location = models.CharField(max_length=100, null=True, verbose_name='محدوده', blank=True)
    address = models.TextField(verbose_name='آدرس', blank=True)
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی', blank=True)

    def __str__(self):
        return self.phone

    @property
    def is_active(self):
        return self.state == User.State.ACTIVE or self.state == User.State.GUEST

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def save(self, *args, **kwargs):
        if not self.id:
            # تولید کد معرف برای کاربر جدید
            self.referral_code = self.generate_referral_code()

        super().save(*args, **kwargs)

    def generate_referral_code(self):
        letters_and_digits = string.ascii_letters + string.digits
        referral_code = ''.join(random.choice(letters_and_digits) for _ in range(8))
        return referral_code


class GuestCounter(models.Model):
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        verbose_name = 'مهمان'
        verbose_name_plural = 'مهمان‌ها'

    def __str__(self):
        return self.id
