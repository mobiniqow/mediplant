# Generated by Django 4.2.3 on 2023-10-19 16:30

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('doctor', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoctorVisit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(choices=[(0, 'Request'), (1, 'Accept'), (2, 'Failed'), (3, 'End'), (4, 'Report')], default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user_rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('doctor_rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('time', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)])),
                ('comment', models.TextField()),
                ('doctor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctor')),
                ('patient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.patientprofile')),
            ],
        ),
    ]