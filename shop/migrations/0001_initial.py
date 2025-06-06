# Generated by Django 5.0 on 2025-05-17 05:16

import ckeditor.fields
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, unique=True, verbose_name='نام فروشگاه')),
                ('trade_id', models.CharField(max_length=19, verbose_name='شناسه تجاری')),
                ('state', models.IntegerField(choices=[(0, 'در انتظار تایید'), (1, 'فعال'), (2, 'غیرفعال'), (3, 'گزارش\u200cشده'), (4, 'نیازمند تکمیل اطلاعات')], default=0, verbose_name='وضعیت فروشگاه')),
                ('shop_home', models.TextField(verbose_name='آدرس فروشگاه')),
                ('national_code', models.CharField(blank=True, max_length=10, unique=True, verbose_name='کد ملی')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('catalog', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='کاتالوگ محصولات')),
                ('rate_state', models.IntegerField(choices=[(0, 'سیاه'), (1, 'سفید'), (2, 'برنزی'), (3, 'طلایی')], default=1, verbose_name='وضعیت امتیازدهی')),
                ('price', models.IntegerField(default=0, verbose_name='قیمت پایه')),
                ('location_lat', models.CharField(default='35.7475', max_length=12, verbose_name='عرض جغرافیایی')),
                ('location_lng', models.CharField(default='51.2358', max_length=12, verbose_name='طول جغرافیایی')),
                ('image', models.FileField(blank=True, null=True, upload_to='shop/image/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='تصویر فروشگاه')),
                ('banner_1', models.FileField(blank=True, null=True, upload_to='shop/banner/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='بنر ۱')),
                ('banner_2', models.FileField(blank=True, null=True, upload_to='shop/banner/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='بنر ۲')),
                ('banner_3', models.FileField(blank=True, null=True, upload_to='shop/banner/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='بنر ۳')),
                ('cert_1', models.FileField(blank=True, null=True, upload_to='shop/cert/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='گواهی\u200cنامه ۱')),
                ('cert_2', models.FileField(blank=True, null=True, upload_to='shop/cert/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='گواهی\u200cنامه ۲')),
                ('shop_phones', models.CharField(blank=True, max_length=30, null=True, verbose_name='شماره تماس')),
                ('start_time', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)], verbose_name='ساعت شروع فعالیت')),
                ('end_time', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(24)], verbose_name='ساعت پایان فعالیت')),
                ('instagram', models.CharField(blank=True, max_length=100, null=True, verbose_name='اینستاگرام')),
                ('whats_app', models.CharField(blank=True, max_length=100, null=True, verbose_name='واتساپ')),
                ('telegram', models.CharField(blank=True, max_length=100, null=True, verbose_name='تلگرام')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'فروشگاه',
                'verbose_name_plural': 'فروشگاه\u200cها',
            },
        ),
        migrations.CreateModel(
            name='ProductNeedToAdded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(1, 'در انتظار بررسی'), (2, 'گزارش\u200cشده'), (3, 'تایید شده'), (4, 'در حال پردازش')], default=1, verbose_name='وضعیت')),
                ('name', models.CharField(max_length=33, unique=True, verbose_name='نام محصول پیشنهادی')),
                ('image', models.FileField(blank=True, upload_to='shop/image/need_product/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='تصویر محصول')),
                ('description', ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='توضیحات محصول')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.shop', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'درخواست افزودن محصول',
                'verbose_name_plural': 'درخواست\u200cهای افزودن محصول',
            },
        ),
        migrations.CreateModel(
            name='ShopProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('capacity', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='ظرفیت موجود')),
                ('inventory_state', models.IntegerField(choices=[(0, 'موجود'), (1, 'ناموجود')], default=1, verbose_name='وضعیت موجودی')),
                ('price', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='قیمت کالا')),
                ('material', models.IntegerField(choices=[(1, 'بسته\u200cبندی'), (2, 'پک'), (3, 'دانه\u200cای'), (4, 'کیلویی'), (5, 'شیشه\u200cای')], default=1, verbose_name='نوع بسته\u200cبندی')),
                ('how_to_use', models.CharField(default='نحوه مصرف', max_length=255, verbose_name='راهنمای مصرف')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.product', verbose_name='محصول')),
                ('shop', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.shop', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'محصول فروشگاه',
                'verbose_name_plural': 'محصولات فروشگاه',
            },
        ),
        migrations.CreateModel(
            name='ShopSettlement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='مبلغ')),
                ('status', models.IntegerField(choices=[(0, 'در انتظار بررسی'), (1, 'تایید شده'), (2, 'رد شده'), (3, 'پرداخت شده')], default=0, verbose_name='وضعیت تسویه')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='آخرین بروزرسانی')),
                ('receipt_image', models.ImageField(blank=True, null=True, upload_to='settlements/receipts/', verbose_name='تصویر رسید پرداخت')),
                ('transaction_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='شناسه تراکنش')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shop', verbose_name='فروشگاه')),
            ],
            options={
                'verbose_name': 'تسویه\u200cحساب فروشگاه',
                'verbose_name_plural': 'تسویه\u200cحساب\u200cهای فروشگاه\u200cها',
            },
        ),
    ]
