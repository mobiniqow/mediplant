from django.db import models
from django.core.validators import FileExtensionValidator


class Banner(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        REPORTED = 2
        DE_ACTIVE = 3
    state = models.IntegerField(choices=State.choices,default=State.SUSPEND)
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
