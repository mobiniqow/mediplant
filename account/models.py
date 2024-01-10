import re
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import SET_NULL
from django_jalali.db import models as jmodels
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

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


class User(AbstractBaseUser, PermissionsMixin):
    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        REPORTED = 2
        BANNED = 3

    class UserActivationState(models.IntegerChoices):
        WHITE = 0
        SILVER = 1
        GOLD = 2

    # created_at = jmodels.jDateField(auto_now_add=True, verbose_name='زمان ساخت')
    # updated_at = jmodels.jDateField(auto_now=True, verbose_name='زمان اخرین ویرایش')
    avatar = models.FileField(upload_to='paccount/user/avatar',
                              validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], blank=True,
                              verbose_name='تصویر')
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت')
    activation_state = models.IntegerField(choices=UserActivationState.choices, default=UserActivationState.WHITE,
                                           verbose_name='نوع پلن')
    user_name = models.CharField(max_length=83, verbose_name='نام و نام خانوادگی')
    phone = models.CharField(max_length=17, unique=True, validators=[phone_validator], verbose_name='شماره تلفن')
    objects = BasicUserManager()
    USERNAME_FIELD = "phone"
    is_staff = models.BooleanField(default=False)
    gender = models.BooleanField(verbose_name='جنسیت')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کدملی')
    email = models.EmailField(verbose_name='ایمیل')
    # birth_day = jmodels.jDateField(verbose_name='تاریخ تولد')
    ref_code = models.CharField(max_length=8, verbose_name='کد معرفی', unique=True)
    # country = models.ForeignKey(Country, on_delete=SET_NULL, null=True, verbose_name='کشور')
    city = models.ForeignKey(City, on_delete=SET_NULL, null=True, verbose_name='شهر')
    location = models.ForeignKey(CityLocation, on_delete=SET_NULL, null=True, verbose_name='محدوده')
    address = models.TextField(verbose_name='ادرس')
    postal_code = models.CharField(max_length=20, verbose_name='کد پستی')

    # point = g_models.PointField(verbose_name='نقشه')

    def __str__(self):
        return self.phone

    @property
    def is_active(self):
        return self.state == User.State.ACTIVE

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'
