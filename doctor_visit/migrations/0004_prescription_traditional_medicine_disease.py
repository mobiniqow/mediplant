# Generated by Django 4.2.3 on 2023-10-20 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sickness', '0001_initial'),
        ('doctor_visit', '0003_alter_doctorvisit_doctor_prescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='traditional_medicine_disease',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sickness.traditionalmedicinedisease', verbose_name='بیمار'),
        ),
    ]