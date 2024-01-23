from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.db.models import SET_NULL

from account.models import User
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
    shop_home = models.TextField( verbose_name='آدرس فروشگاه')
    image = models.FileField(upload_to="shop/image/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                             verbose_name='تصویر')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کدملی', blank=True)
    description = models.TextField(verbose_name='توضیحات')
    rate_state = models.IntegerField(choices=ShopRate.choices, default=ShopRate.WHITE, verbose_name='وضعیت امتیاز')

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

    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')
    capacity = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='ظرفیت')
    inventory_state = models.IntegerField(choices=Inventory.choices, default=Inventory.NOT_AVAILABLE,
                                          verbose_name='وضعیت موجودی')
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='قیمت')

    class Meta:
        verbose_name = 'محصول فروشگاه'
        verbose_name_plural = 'محصولات فروشگاه'

    def __str__(self):
        return self.shop.name
