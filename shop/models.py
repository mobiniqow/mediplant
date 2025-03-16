from django.core.validators import FileExtensionValidator, MinValueValidator
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
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name='کاربر')
    shop_home = models.TextField(verbose_name='آدرس فروشگاه')
    image = models.FileField(upload_to="shop/image/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                             verbose_name='تصویر')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کدملی', blank=True)
    description = models.TextField(verbose_name='توضیحات')
    catalog = RichTextField(blank=True, null=True, verbose_name='کاتالوگ')
    rate_state = models.IntegerField(choices=ShopRate.choices, default=ShopRate.WHITE, verbose_name='وضعیت امتیاز')
    price = models.IntegerField(verbose_name='واحد قیمت بر حسب واحد', default=0)
    location_lat = models.CharField(max_length=12, default="35.7475")
    location_lng = models.CharField(max_length=12, default="51.2358")

    # location = gis_models.PointField(null=True, blank=True, verbose_name='موقعیت مکانی',)

    # def save(self, *args, **kwargs):
    #     from django.contrib.gis.geos import Point
    # تبدیل عرض و طول جغرافیایی به یک نقطه
    # self.location = Point(float(self.location_lat), float(self.location_lng))
    # super().save(*args, **kwargs)
    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه‌ها'


class ShopImage(models.Model):
    shop = models.ForeignKey(Shop, on_delete=SET_NULL, null=True, verbose_name='فروشگاه')
    image = models.FileField(upload_to="shop/images/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                             verbose_name='تصویر  ')

    class Meta:
        verbose_name = 'تصویر فروشگاه'
        verbose_name_plural = 'تصاویر فروشگاه'


class CertificateImage(models.Model):
    shop = models.ForeignKey(Shop, on_delete=SET_NULL, null=True, verbose_name='فروشگاه')
    certificate_image = models.FileField(upload_to="shop/certificate/",
                                         validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                                         verbose_name='تصویر مجوز')

    class Meta:
        verbose_name = 'تصویر فروشگاه'
        verbose_name_plural = 'تصاویر فروشگاه'


class ShopPhone(models.Model):
    shop = models.ForeignKey(Shop, on_delete=SET_NULL, null=True, verbose_name='فروشگاه')
    phone = models.CharField(max_length=13, verbose_name='تلفن', unique=True)

    class Meta:
        verbose_name = 'تلفن فروشگاه'
        verbose_name_plural = 'تلفن‌های فروشگاه'


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
