# Generated by Django 4.2.3 on 2023-09-12 04:44

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleEncyclopedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='عنوان')),
                ('created_at', django_jalali.db.models.jDateField(auto_now_add=True, verbose_name='تاریخ ساخت')),
                ('abstract', ckeditor.fields.RichTextField()),
                ('content', ckeditor.fields.RichTextField()),
                ('registered', models.CharField(max_length=140, verbose_name='ثبت در')),
            ],
            options={
                'verbose_name': 'دانشنامه مقاله',
                'verbose_name_plural': 'دانشنامه مقاله ها',
            },
        ),
        migrations.CreateModel(
            name='ArticleReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='عنوان')),
            ],
            options={
                'verbose_name': 'مرجع',
                'verbose_name_plural': 'مراجع',
            },
        ),
        migrations.CreateModel(
            name='EncyclopediaArticle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encyclopedia.articleencyclopedia', verbose_name='مقاله')),
                ('reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='encyclopedia.articlereference', verbose_name='منبع')),
            ],
            options={
                'verbose_name': 'مرجع مقاله',
                'verbose_name_plural': 'مراجع مقاله',
            },
        ),
        migrations.CreateModel(
            name='ArticleEncyclopediaCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='عنوان')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='encyclopedia.articleencyclopediacategory', verbose_name='منبع')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.AddField(
            model_name='articleencyclopedia',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='encyclopedia.articleencyclopediacategory', verbose_name='دسته بندی'),
        ),
    ]