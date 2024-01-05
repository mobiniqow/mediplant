from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import SET_NULL


class ClassId(models.Model):
    name = models.CharField(max_length=22)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "شناسه صنف"
        verbose_name_plural = "شناسه های صنف"


class Product(models.Model):
    class Type(models.IntegerChoices):
        GIAH = 0
        ARAGH = 1
        ROGHAN = 2
        AFSHORE = 3
        SHARBAT = 4
        GHORS = 5
        KAPSOL = 6
        SAMGH = 7
        GOL = 8
        DANE = 9
        BARG = 10
        SAGHE = 11
        RISHE = 12
        POST = 13
        MIVE = 14
        POMAD = 15
        ZOMAD = 16
        PODR = 17
        HASTE = 18
        KERM = 19
        MOKAMEL = 20
        SHOYANDE = 21
        BOKHORI = 22
        DOD_KARDANI = 23

    class Material(models.IntegerChoices):
        BASTE_BANDI = 1
        PACK = 2
        DANE_E = 3
        KILOE = 4
        SHISHE_E = 5

    class State(models.IntegerChoices):
        SUSPEND = 0
        ACTIVE = 1
        DE_ACTIVE = 2

    trade_id = models.CharField(max_length=19, verbose_name='شناسه بازرگانی')
    class_id = models.ForeignKey(ClassId, on_delete=SET_NULL, null=True, verbose_name='شناسه صنف')
    category = models.ForeignKey('Category', on_delete=SET_NULL, null=True, verbose_name='کتگوری')
    name = models.CharField(max_length=33, verbose_name="نام کالا", unique=True)
    type = models.IntegerField(choices=Type.choices, verbose_name='نوع کالا')
    material = models.IntegerField(choices=Material.choices, verbose_name='جنس کالا')
    description = models.TextField(verbose_name='جنس کالا', )
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
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
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


class Category(models.Model):
    name = models.CharField(max_length=40)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
