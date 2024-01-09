# Generated by Django 4.2.3 on 2024-01-09 00:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_category_product_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'دسته بندی', 'verbose_name_plural': 'دسته بندی ها'},
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.FileField(default=1, upload_to='product/image', validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg', 'svg'])], verbose_name='تصاویر'),
            preserve_default=False,
        ),
    ]
