# Generated by Django 4.2.3 on 2023-10-20 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('encyclopedia', '0007_alter_herbalencyclopediaimage_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encyclopediaofdiseases',
            name='reference',
        ),
        migrations.CreateModel(
            name='EncyclopediaOfDiseasesReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('herbal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encyclopedia.encyclopediaofdiseases')),
                ('refrence', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encyclopedia.articlereference')),
            ],
            options={
                'verbose_name': 'ارجاع',
                'verbose_name_plural': 'ارجاعات',
            },
        ),
    ]