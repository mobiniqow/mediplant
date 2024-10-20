# Generated by Django 4.2.3 on 2024-08-06 03:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='consumption_instruction',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='نحوه مصرف'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, null=True, verbose_name='معرفی محصول'),
        ),
    ]