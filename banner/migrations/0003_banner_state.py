# Generated by Django 4.2 on 2024-01-08 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0002_alter_banner_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='state',
            field=models.IntegerField(choices=[(0, 'Suspend'), (1, 'Active'), (2, 'Reported'), (3, 'De Active')], default=0),
        ),
    ]