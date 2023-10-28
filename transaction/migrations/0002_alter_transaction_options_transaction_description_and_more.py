# Generated by Django 4.2.3 on 2023-10-19 17:29

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'verbose_name': 'تراکنش', 'verbose_name_plural': 'تراکنش\u200cها'},
        ),
        migrations.AddField(
            model_name='transaction',
            name='description',
            field=models.TextField(blank=True, verbose_name='توضیحات'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='payment_gateway',
            field=models.CharField(default=1, max_length=50, verbose_name='نام درگاه پرداخت'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_number',
            field=models.CharField(default=1, max_length=20, verbose_name='شماره تراکنش'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='مبلغ'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='state',
            field=models.IntegerField(choices=[(0, 'Suspend'), (1, 'Payment Gateway'), (2, 'Failed'), (3, 'Successful'), (4, 'Reported')], default=0, verbose_name='وضعیت'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر'),
        ),
    ]
