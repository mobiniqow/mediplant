# Generated by Django 5.0 on 2025-05-17 05:16

import account.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestCounter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_key', models.CharField(blank=True, max_length=40, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'مهمان',
                'verbose_name_plural': 'مهمان\u200cها',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('role', models.IntegerField(choices=[(1, 'کاربر'), (2, 'پزشک'), (3, 'فروشنده')], default=1)),
                ('avatar', models.FileField(blank=True, upload_to='paccount/user/avatar', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg'])], verbose_name='تصویر')),
                ('state', models.IntegerField(choices=[(0, 'Suspend'), (1, 'Active'), (2, 'Reported'), (3, 'Banned'), (4, 'Guest')], default=0, verbose_name='وضعیت')),
                ('gender', models.IntegerField(choices=[(1, 'مرد'), (0, 'زن')], default=1, verbose_name=' ')),
                ('activation_state', models.IntegerField(choices=[(0, 'White'), (1, 'Silver'), (2, 'Gold')], default=0, verbose_name='نوع پلن')),
                ('user_name', models.CharField(blank=True, max_length=83, verbose_name='نام و نام خانوادگی')),
                ('phone', models.CharField(max_length=17, unique=True, validators=[account.models.phone_validator], verbose_name='شماره تلفن')),
                ('phone_otp', models.CharField(blank=True, max_length=6, null=True, verbose_name='OTP for phone verification')),
                ('email_otp', models.CharField(blank=True, max_length=6, null=True, verbose_name='OTP for email verification')),
                ('phone_otp_sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Time when phone OTP was sent')),
                ('email_otp_sent_at', models.DateTimeField(blank=True, null=True, verbose_name='Time when email OTP was sent')),
                ('is_staff', models.BooleanField(default=False)),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='ایمیل')),
                ('referral_code', models.CharField(editable=False, max_length=8, unique=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True, verbose_name='شهر')),
                ('location', models.CharField(blank=True, max_length=100, null=True, verbose_name='محدوده')),
                ('address', models.TextField(blank=True, verbose_name='آدرس')),
                ('postal_code', models.CharField(blank=True, max_length=20, verbose_name='کد پستی')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'کاربر',
                'verbose_name_plural': 'کاربران',
            },
        ),
    ]
