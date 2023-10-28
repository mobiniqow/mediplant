# Generated by Django 4.2.3 on 2023-10-19 16:48

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0002_shop_rate_state_shop_trade_id_shopproduct_shopphone'),
        ('sale', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salebasket',
            options={'verbose_name': 'سبد خرید', 'verbose_name_plural': 'سبد\u200cهای خرید'},
        ),
        migrations.AlterModelOptions(
            name='salebasketproduct',
            options={'verbose_name': 'محصول سبد خرید', 'verbose_name_plural': 'محصولات سبد خرید'},
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='address',
            field=models.TextField(verbose_name='آدرس'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='discount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='تخفیف'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='قیمت'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.shop', verbose_name='فروشگاه'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='state',
            field=models.IntegerField(choices=[(0, 'Suspend'), (1, 'In Pay'), (2, 'Pay Failed'), (3, 'Pay Success'), (4, 'In Shop Compilation'), (5, 'Sending'), (6, 'Send Back'), (7, 'In Post Office'), (8, 'Done And Finish'), (9, 'Cancelled')], default=0, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='transaction.transaction', verbose_name='تراکنش'),
        ),
        migrations.AlterField(
            model_name='salebasket',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
        migrations.AlterField(
            model_name='salebasketproduct',
            name='basket',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sale.salebasket', verbose_name='سبد خرید'),
        ),
        migrations.AlterField(
            model_name='salebasketproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='salebasketproduct',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.shopproduct', verbose_name='محصول'),
        ),
        migrations.AlterField(
            model_name='salebasketproduct',
            name='unit',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='تعداد'),
        ),
    ]
