from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import SET_NULL
from ckeditor.fields import RichTextField

from account.models import User
from product.models import Product


class Shop(models.Model):
    class ShopStatus(models.IntegerChoices):
        PENDING = 0, "در انتظار تایید"
        ACTIVE = 1, 'فعال'
        DE_ACTIVE = 2, 'غیرفعال'
        REPORTED = 3, 'گزارش‌شده'
        NEED_TO_COMPLETE = 4, 'نیازمند تکمیل اطلاعات'

    class ShopRate(models.IntegerChoices):
        BLACK = 0, 'سیاه'
        WHITE = 1, 'سفید'
        BRONZE = 2, 'برنزی'
        GOLD = 3, 'طلایی'

    name = models.CharField(max_length=40, verbose_name='نام فروشگاه', unique=True)
    trade_id = models.CharField(max_length=19, verbose_name='شناسه تجاری')
    state = models.IntegerField(choices=ShopStatus.choices, default=ShopStatus.PENDING, verbose_name='وضعیت فروشگاه')
    user = models.ForeignKey(User, on_delete=SET_NULL, null=True, verbose_name='کاربر', unique=True)
    shop_home = models.TextField(verbose_name='آدرس فروشگاه')
    national_code = models.CharField(max_length=10, unique=True, verbose_name='کد ملی', blank=True)
    description = models.TextField(verbose_name='توضیحات')
    catalog = RichTextField(blank=True, null=True, verbose_name='کاتالوگ محصولات')
    rate_state = models.IntegerField(choices=ShopRate.choices, default=ShopRate.WHITE, verbose_name='وضعیت امتیازدهی')
    price = models.IntegerField(verbose_name='قیمت پایه', default=0)
    location_lat = models.CharField(max_length=12, default="35.7475", verbose_name='عرض جغرافیایی')
    location_lng = models.CharField(max_length=12, default="51.2358", verbose_name='طول جغرافیایی')
    image = models.FileField(upload_to="shop/image/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                             verbose_name='تصویر فروشگاه', null=True, blank=True)
    banner_1 = models.FileField(upload_to="shop/banner/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                                verbose_name='بنر ۱', null=True, blank=True)
    banner_2 = models.FileField(upload_to="shop/banner/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                                verbose_name='بنر ۲', null=True, blank=True)
    banner_3 = models.FileField(upload_to="shop/banner/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                                verbose_name='بنر ۳', null=True, blank=True)
    cert_1 = models.FileField(upload_to="shop/cert/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                              verbose_name='گواهی‌نامه ۱', null=True, blank=True)
    cert_2 = models.FileField(upload_to="shop/cert/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                              verbose_name='گواهی‌نامه ۲', null=True, blank=True)
    shop_phones = models.CharField(max_length=30, null=True, blank=True, verbose_name='شماره تماس')
    start_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)],
                                     null=True, blank=True, verbose_name='ساعت شروع فعالیت')
    end_time = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)],
                                   null=True, blank=True, verbose_name='ساعت پایان فعالیت')
    instagram = models.CharField(max_length=100, null=True, blank=True, verbose_name='اینستاگرام')
    whats_app = models.CharField(max_length=100, null=True, blank=True, verbose_name='واتساپ')
    telegram = models.CharField(max_length=100, null=True, blank=True, verbose_name='تلگرام')

    class Meta:
        verbose_name = 'فروشگاه'
        verbose_name_plural = 'فروشگاه‌ها'

    def __str__(self):
        return self.name


class ShopProduct(models.Model):
    class Inventory(models.IntegerChoices):
        AVAILABLE = 0, 'موجود'
        NOT_AVAILABLE = 1, 'ناموجود'

    class Material(models.IntegerChoices):
        BASTE_BANDI = 1, 'بسته‌بندی'
        PACK = 2, 'پک'
        DANE_E = 3, 'دانه‌ای'
        KILOE = 4, 'کیلویی'
        SHISHE_E = 5, 'شیشه‌ای'

    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')
    capacity = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='ظرفیت موجود')
    inventory_state = models.IntegerField(choices=Inventory.choices, default=Inventory.NOT_AVAILABLE,
                                          verbose_name='وضعیت موجودی')
    price = models.IntegerField(validators=[MinValueValidator(0)], default=0, verbose_name='قیمت کالا')
    material = models.IntegerField(choices=Material.choices, default=Material.BASTE_BANDI,
                                   verbose_name='نوع بسته‌بندی')
    how_to_use = models.CharField(max_length=255, default="نحوه مصرف", verbose_name='راهنمای مصرف')

    class Meta:
        verbose_name = 'محصول فروشگاه'
        verbose_name_plural = 'محصولات فروشگاه'

    def __str__(self):
        return f"{self.product.name} - {self.shop.name}"


class ProductNeedToAdded(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 1, 'در انتظار بررسی'
        REPORT = 2, 'گزارش‌شده'
        ACCEPT = 3, 'تایید شده'
        IN_PROGRES = 4, 'در حال پردازش'

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name="وضعیت")
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه')
    name = models.CharField(max_length=33, unique=True, verbose_name="نام محصول پیشنهادی")
    image = models.FileField(upload_to='shop/image/need_product/',
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg'])],
                             blank=True, verbose_name='تصویر محصول')
    description = RichTextField(blank=True, null=True, verbose_name='توضیحات محصول')

    class Meta:
        verbose_name = "درخواست افزودن محصول"
        verbose_name_plural = "درخواست‌های افزودن محصول"

    def __str__(self):
        return self.name


class ShopSettlement(models.Model):
    class STATUS(models.IntegerChoices):
        PENDING = 0, "در انتظار بررسی"
        APPROVED = 1, "تایید شده"
        REJECTED = 2, "رد شده"
        PAID = 3, "پرداخت شده"

    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="فروشگاه")
    amount = models.PositiveIntegerField(validators=[MinValueValidator(1)], verbose_name="مبلغ")
    status = models.IntegerField(choices=STATUS.choices, default=STATUS.PENDING, verbose_name="وضعیت تسویه")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="آخرین بروزرسانی")
    receipt_image = models.ImageField(upload_to="settlements/receipts/", null=True, blank=True,
                                      verbose_name="تصویر رسید پرداخت")
    transaction_id = models.CharField(max_length=50, null=True, blank=True, verbose_name="شناسه تراکنش")

    class Meta:
        verbose_name = "تسویه‌حساب فروشگاه"
        verbose_name_plural = "تسویه‌حساب‌های فروشگاه‌ها"

    def __str__(self):
        return f"{self.shop.name} | {self.amount} تومان | {self.get_status_display()}"
