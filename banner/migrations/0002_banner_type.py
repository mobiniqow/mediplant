# Generated by Django 4.2.3 on 2024-08-04 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='banner',
            name='type',
            field=models.IntegerField(choices=[(1, 'Index Top Slider'), (2, 'Index Two Slider'), (3, 'Index Middle Slider'), (4, 'Index Bottom Slider'), (5, 'Search Top Two Banner')], default=1),
        ),
    ]
