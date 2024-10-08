# Generated by Django 4.2.3 on 2024-01-17 08:13

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DockterBranch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=33, unique=True, verbose_name='نام')),
            ],
            options={
                'verbose_name': 'شاخه پزشکی',
                'verbose_name_plural': 'شاخه\u200cهای پزشکی',
            },
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.TextField(verbose_name='آدرس')),
                ('state', models.IntegerField(choices=[(0, 'Suspend'), (1, 'Active'), (2, 'De Active'), (3, 'Reported'), (4, 'Banned')], default=0, verbose_name='وضعیت')),
                ('picture', models.FileField(blank=True, upload_to='doctor/avatar', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='تصویر پرسنلی')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('id_active', models.BooleanField(verbose_name='وضعیت فعالیت')),
                ('register_time', models.IntegerField(verbose_name='مهلت ثبت نام')),
                ('responsiveness', models.IntegerField(choices=[(0, 'Dark'), (1, 'White'), (2, 'Silver'), (3, 'Gold')], default=1, verbose_name='نوع عملکرد')),
                ('postal_code', models.CharField(max_length=12, verbose_name='کد پستی')),
                ('shaba', models.CharField(max_length=12, verbose_name='شماره شبا')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor.dockterbranch', verbose_name='شاخه تحصیلی')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پزشک',
                'verbose_name_plural': 'پزشکان',
            },
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('history', models.TextField(max_length=33, verbose_name='تاریخچه')),
            ],
            options={
                'verbose_name': 'تاریخچه',
                'verbose_name_plural': 'تاریخچه\u200cها',
            },
        ),
        migrations.CreateModel(
            name='PatientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor', verbose_name='پزشک')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'پروفایل بیمار',
                'verbose_name_plural': 'پروفایل بیماران',
            },
        ),
        migrations.CreateModel(
            name='DoctorVisitPrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='قیمت')),
                ('timing', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='زمان')),
                ('state', models.IntegerField(choices=[(0, 'Suspend'), (1, 'Active'), (2, 'De Active')], verbose_name='وضعیت')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor', verbose_name='پزشک')),
            ],
            options={
                'verbose_name': 'قیمت و زمان ویزیت دکتر',
                'verbose_name_plural': 'قیمت و زمان ویزیت\u200cهای دکتر',
            },
        ),
        migrations.CreateModel(
            name='DoctorHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor', verbose_name='پزشک')),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='doctor.history', verbose_name='تاریخچه')),
            ],
            options={
                'verbose_name': 'تاریخچه دکتر',
                'verbose_name_plural': 'تاریخچه\u200cهای دکتر',
            },
        ),
        migrations.CreateModel(
            name='DocktorPhone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, verbose_name='شماره تلفن')),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor.doctor', verbose_name='پزشک')),
            ],
            options={
                'verbose_name': 'شماره تلفن پزشک',
                'verbose_name_plural': 'شماره تلفن\u200cهای پزشک',
            },
        ),
    ]
