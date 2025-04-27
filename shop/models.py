from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL
from ckeditor.fields import RichTextField
# from django.contrib.gis.db import models as gis_models

from account.models import User
from feedback.models import FeedbackObject
from product.models import Product


class Shop(models.Model):
    class ShopStatus(models.IntegerChoices):
        PENDING = 0, "انتظار"
        ACTIVE = 1, 'فعال'
        DE_ACTIVE = 2, 'غیر فعال'
        REPORTED = 3, 'گزارش شده'
        NEED_TO_COMPLETE = 4, 'نیاز به تکمیل پروفایل'

    class ShopRate(models.IntegerChoices):
        BLACK = 0, 'سیاه'
        WHITE = 1, 'سفید'
        BRONZE = 2, 'برنز'
        GOLD = 3, 'طلایی'

    name = models.CharField(max_length=40, verbose_name='نام', unique=True)
    trade_id = models.CharField(max_length=19, verbose_name='شناسه تجاری')
    state = models.IntegerField(choices=ShopStatus.choices, default=ShopStatus.PENDING, verbose_name='وضعیت')
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name='کاربر',unique=True)
    shop_home = models.TextField(verbose_name='آدرس فروشگاه')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کدملی', blank=True)
    description = models.TextField(verbose_name='توضیحات')
    catalog = RichTextField(blank=True, null=True, verbose_name='کاتالوگ')
    rate_state = models.IntegerField(choices=ShopRate.choices, default=ShopRate.WHITE, verbose_name='وضعیت امتیاز')
    price = models.IntegerField(verbose_name='واحد قیمت بر حسب واحد', default=0)
    location_lat = models.CharField(max_length=12, default="35.7475")
    location_lng = models.CharField(max_length=12, default="51.2358")
    image = models.FileField(upload_to="shop/image/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                             verbose_name='تصویر', null=True, blank=True)
    banner_1 = models.FileField(upload_to="shop/banner/",
                                validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], null=True, blank=True)
    banner_2 = models.FileField(upload_to="shop/banner/",
                                validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], null=True, blank=True)
    banner_3 = models.FileField(upload_to="shop/banner/",
                                validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], null=True, blank=True)
    cert_1 = models.FileField(upload_to="shop/cert/",
                              validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], null=True, blank=True)
    cert_2 = models.FileField(upload_to="shop/cert/",
                              validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], null=True, blank=True)
    shop_phones = models.CharField(max_length=30, null=True, blank=True)
    start_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)], null=True, blank=True)
    end_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)], null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    whats_app = models.CharField(max_length=100, null=True, blank=True)
    telegram = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه‌ها'


class ShopProduct(models.Model):
    class Inventory(models.IntegerChoices):
        AVAILABLE = 0, 'در دسترس'
        NOT_AVAILABLE = 1, 'در دسترس نیست'

    class Material(models.IntegerChoices):
        BASTE_BANDI = 1, 'بسته بندی'
        PACK = 2, 'پک'
        DANE_E = 3, 'دانه ای'
        KILOE = 4, 'کیلوای'
        SHISHE_E = 5, 'شیشه ای'

    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه')

    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    capacity = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='ظرفیت')

    inventory_state = models.IntegerField(choices=Inventory.choices, default=Inventory.NOT_AVAILABLE,
                                          verbose_name='وضعیت موجودی')

    price = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='قیمت')

    material = models.IntegerField(choices=Material.choices, verbose_name='جنس کالا', default=Material.BASTE_BANDI)

    how_to_use = models.CharField(max_length=255, default="نحوه مصرف")

    class Meta:
        verbose_name = 'محصول فروشگاه'
        verbose_name_plural = 'محصولات فروشگاه'

    def __str__(self):
        return self.shop.name


class ProductNeedToAdded(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 1
        REPORT = 2
        ACCEPT = 3
        IN_PROGRES = 4

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه')
    name = models.CharField(max_length=33, verbose_name="نام کالا", unique=True)
    image = models.FileField(upload_to='shop/image/need_product/',
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ], blank=True,
                             verbose_name='تصویر')
    description = RichTextField(blank=True, null=True, verbose_name='معرفی محصول')


class ShopSettlement(models.Model):
    class STATUS(models.IntegerChoices):
        PENDING = 0, "در انتظار بررسی"
        APPROVED = 1, "تایید شده"
        REJECTED = 2, "رد شده"
        PAID = 3, "پرداخت شده"

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="فروشگاه")
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="مبلغ درخواستی")
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.PENDING,
                                 verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ درخواست")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین تغییر وضعیت")
    receipt_image = models.ImageField(upload_to="settlements/receipts/", null=True, blank=True,
                                      verbose_name="تصویر فیش پرداختی")
    transaction_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="شناسه تراکنش")

    def __str__(self):
        return f"تسویه حساب {self.shop.name} - {self.amount} تومان - {self.get_status_display()}"
