from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from account.models import User


class ChatSession(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'جلسه چت'
        verbose_name_plural = 'جلسات چت'


class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, verbose_name='جلسه چت')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='فرستنده')
    content = models.TextField(verbose_name='محتوا')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام‌ها'


class Shop(models.Model):
    chat_sessions = GenericRelation(ChatSession, content_type_field='content_type', object_id_field='object_id')


class Doctor(models.Model):
    chat_sessions = GenericRelation(ChatSession, content_type_field='content_type', object_id_field='object_id')
