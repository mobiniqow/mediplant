# Generated by Django 4.2.3 on 2024-01-17 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='referral_code',
            field=models.CharField(default=1, editable=False, max_length=8, unique=True),
            preserve_default=False,
        ),
    ]
