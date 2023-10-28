# Generated by Django 4.2.3 on 2023-10-20 03:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0003_alter_patientprofile_options'),
        ('doctor_visit', '0002_alter_doctorvisit_options_alter_doctorvisit_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorvisit',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='doctor.doctorvisitprice', verbose_name='پزشک'),
        ),
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='تاریخ به\u200cروزرسانی')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('therapy', models.TextField(verbose_name='دارو و درمان')),
                ('doctor_visit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='doctor_visit.doctorvisit')),
            ],
            options={
                'verbose_name': 'نسخه بیمار',
                'verbose_name_plural': 'نسخه های بیمار',
            },
        ),
    ]
