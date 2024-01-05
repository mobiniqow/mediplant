from django.db import models
from django.core.validators import FileExtensionValidator


class Banner(models.Model):
    name = models.CharField(max_length=70, verbose_name='نام')
    image = models.FileField(upload_to="banner/images/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                             verbose_name='تصویر')
    link_url = models.TextField(verbose_name='آدرس لینک')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
