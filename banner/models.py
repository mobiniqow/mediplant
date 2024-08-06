from django.db import models
from django.core.validators import FileExtensionValidator


class Banner(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        REPORTED = 2
        DE_ACTIVE = 3

    class Type(models.IntegerChoices):
        INDEX_TOP_SLIDER = 1
        INDEX_TWO_SLIDER = 2
        INDEX_MIDDLE_SLIDER = 3
        INDEX_BOTTOM_SLIDER = 4
        SEARCH_TOP_TWO_BANNER = 5

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    name = models.CharField(max_length=70, verbose_name='نام')
    image = models.FileField(upload_to="banner/images/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg']), ],
                             verbose_name='تصویر')
    link_url = models.TextField(verbose_name='آدرس لینک')
    content = models.TextField(verbose_name='متن', blank=True)
    type = models.IntegerField(choices=Type.choices, default=Type.INDEX_TOP_SLIDER)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'بنر'
        verbose_name_plural = 'بنرها'
