# Generated by Django 4.2 on 2024-01-10 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0013_alter_articleencyclopediacategory_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articleencyclopedia',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='تاریخ ساخت'),
        ),
    ]
