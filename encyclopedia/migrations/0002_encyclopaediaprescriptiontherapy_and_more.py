# Generated by Django 4.2.3 on 2023-09-12 08:26

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EncyclopaediaPrescriptionTherapy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='عنوان')),
                ('reason_for_consumption', models.TextField(verbose_name='علت مصرف')),
                ('prescription_compounds', models.TextField(verbose_name='ترکیبات نسخه')),
                ('the_amount_of_compounds', models.TextField(verbose_name='میزان ترکیبات')),
                ('who_to_use', models.TextField(verbose_name='طریقه مصرف')),
                ('complications_of_compounds', models.TextField(verbose_name='عوارض ترکیبات')),
                ('prescription_complications', models.TextField(verbose_name='عوارض کلی نسخه')),
                ('version_reference', models.TextField(verbose_name='مرجع نسخه')),
            ],
            options={
                'verbose_name': 'دانشنامه نسخ درمانی',
                'verbose_name_plural': 'دانشنامه نسخ درمانی',
            },
        ),
        migrations.CreateModel(
            name='EncyclopediaCombinedDrugs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='عنوان')),
                ('classification', models.CharField(max_length=100, verbose_name='طبقه بندی')),
                ('latin_name', models.CharField(max_length=100, verbose_name='نام لاتین')),
                ('bomi', models.TextField(verbose_name='بومی')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('compounds', models.TextField(verbose_name='ترکیبات')),
                ('amount_of_compounds', models.TextField(verbose_name='مقدار ترکیبات')),
                ('indications', models.TextField(verbose_name='موارد مصرف')),
                ('prohibited_usage', models.TextField(verbose_name='موارد منع مصرف')),
                ('complications', models.TextField(verbose_name='عوارض')),
                ('pregnancy', models.TextField(verbose_name='بارداری')),
                ('method_of_drug_production', models.TextField(verbose_name='روش تولید دارو')),
                ('how_to_use', models.TextField(verbose_name='طریقه مصرف')),
                ('treatment_duration', models.TextField(verbose_name='طول درمان')),
                ('pharmaceutical_supplements', models.TextField(verbose_name='مکمل های دارویی')),
                ('the_nature_of_the_drug', models.CharField(max_length=50, verbose_name='طبیعت دارو')),
                ('drug_manufacturing_company', models.TextField(verbose_name='شرکت تولید کننده دارو')),
                ('articles', models.TextField(verbose_name='مقالات')),
            ],
            options={
                'verbose_name': 'دانشنامه داروهای ترکیبی',
                'verbose_name_plural': 'دانشنامه داروهای ترکیبی',
            },
        ),
        migrations.AlterModelOptions(
            name='articleencyclopedia',
            options={'verbose_name': 'دانشنامه مقاله', 'verbose_name_plural': 'دانشنامه مقالات'},
        ),
        migrations.CreateModel(
            name='EncyclopediaCombinedDrugsImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.FileField(upload_to='EncyclopediaCombinedDrugs/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'svg', 'jpeg'])])),
                ('encyclopedia', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='encyclopedia.encyclopediacombineddrugs')),
            ],
            options={
                'verbose_name': 'دانشنامه داروهای ترکیبی',
                'verbose_name_plural': 'دانشنامه داروهای ترکیبی',
            },
        ),
    ]
