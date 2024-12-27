from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import SET_NULL
from ckeditor.fields import RichTextField

class ClassId(models.Model):
    name = models.CharField(max_length=22)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "شناسه صنف"
        verbose_name_plural = "شناسه های صنف"


class Product(models.Model):
    class Type(models.IntegerChoices):
        GIAH = 0, 'گیاه'
        ARAGH = 1, 'عرق'
        ROGHAN = 2, 'روغن'
        AFSHORE = 3, 'افشوره'
        SHARBAT = 4, 'شربت'
        GHORS = 5, 'قرص'
        KAPSOL = 6, 'کپسول'
        SAMGH = 7, 'سمق'
        GOL = 8, 'گل'
        DANE = 9, 'دانه'
        BARG = 10, 'برگ'
        SAGHE = 11, 'ساقه'
        RISHE = 12, 'ریشه'
        POST = 13, 'پوست'
        MIVE = 14, 'میوه'
        POMAD = 15, 'پماد'
        ZOMAD = 16, 'ضماد'
        PODR = 17, 'پودر'
        HASTE = 18, 'هسته'
        KERM = 19, 'کرم'
        MOKAMEL = 20, 'مکمل'
        SHOYANDE = 21, 'شوینده'
        BOKHORI = 22, 'بخور'
        DOD_KARDANI = 23, 'دود کردنی'

    class State(models.IntegerChoices):
        SUSPEND = 0, 'معلق'
        ACTIVE = 1, 'فعال'
        DE_ACTIVE = 2, 'غیر فعال'

    trade_id = models.CharField(max_length=19, verbose_name='شناسه بازرگانی')
    class_id = models.ForeignKey(ClassId, on_delete=SET_NULL, null=True, verbose_name='شناسه صنف')
    category = models.ForeignKey('Category', on_delete=SET_NULL, null=True, verbose_name='کتگوری', blank=True)
    name = models.CharField(max_length=33, verbose_name="نام کالا", unique=True)
    type = models.IntegerField(choices=Type.choices, verbose_name='نوع کالا')
    description = RichTextField(blank=True,null=True, verbose_name='معرفی محصول')
    consumption_instruction = RichTextField(blank=True, null=True, verbose_name='نحوه مصرف')
    price = models.IntegerField(verbose_name='واحد قیمت بر حسب واحد')
    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name='وضعیت کالا')
    is_active = models.BooleanField(default=False, verbose_name='فعال بودن')
    unit = models.ForeignKey('ProductUnit', on_delete=SET_NULL, null=True, verbose_name='شناسه واحد')

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول',
                                related_name='images')
    image = models.FileField(upload_to='product/image',
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'svg'])], verbose_name='تصاویر')

    class Meta:
        verbose_name = "عکس محصول"
        verbose_name_plural = "عکس محصول"


class ProductUnit(models.Model):
    name = models.CharField(max_length=22, unique=True)

    class Meta:
        verbose_name = "واحد"
        verbose_name_plural = "واحد ها"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to='product/image',
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'svg'])], verbose_name='تصاویر')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
