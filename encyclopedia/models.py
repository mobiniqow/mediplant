from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import SET_NULL, CASCADE

from ckeditor.fields import RichTextField
from django_jalali.db import models as jmodels


class ArticleEncyclopediaCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name="عنوان", unique=True)
    parent = models.ForeignKey("ArticleEncyclopediaCategory", on_delete=SET_NULL, blank=True, null=True,
                               verbose_name="منبع")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

    def __str__(self):
        return self.name


class ArticleReference(models.Model):
    name = models.CharField(max_length=100, verbose_name="عنوان", unique=True)

    class Meta:
        verbose_name = "مرجع"
        verbose_name_plural = "مراجع"

    def __str__(self):
        return self.name


class EncyclopediaArticle(models.Model):
    reference = models.ForeignKey("ArticleReference", on_delete=models.CASCADE, verbose_name="منبع")
    article = models.ForeignKey("ArticleEncyclopedia", on_delete=models.CASCADE, verbose_name="مقاله")

    class Meta:
        verbose_name = "مرجع مقاله"
        verbose_name_plural = "مراجع مقاله"


class NewsPaperEncyclopedia(models.Model):
    logo = models.FileField(upload_to="logo/encyclopedia/new-paper")
    name = models.CharField(max_length=100, verbose_name="نویسنده", unique=True)
    link = models.TextField()


class ArticleEncyclopedia(models.Model):
    name = models.CharField(max_length=100, verbose_name="عنوان", unique=True)
    category = models.ForeignKey("ArticleEncyclopediaCategory", on_delete=SET_NULL,
                                 null=True, verbose_name="دسته بندی")
    created_at = jmodels.jDateField(auto_now_add=True, verbose_name="تاریخ ساخت")
    author = models.CharField(max_length=100, verbose_name="نویسنده", )
    abstract = RichTextField()
    content = RichTextField()
    image = models.FileField(upload_to="article-encyclopedia/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'svg', 'jpeg'])], verbose_name='تصویر')
    registered = models.CharField(max_length=140, verbose_name="ثبت در")

    class Meta:
        verbose_name = "دانشنامه مقاله"
        verbose_name_plural = "دانشنامه مقالات"

    def __str__(self):
        return self.name


class EncyclopaediaPrescriptionTherapy(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        REPORT = 1
        FAILED = 2
        ACCEPT = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)

    name = models.CharField(max_length=100, verbose_name="عنوان", unique=True)
    reason_for_consumption = models.TextField(verbose_name="علت مصرف")
    prescription_compounds = models.TextField(verbose_name="ترکیبات نسخه", unique=True)
    the_amount_of_compounds = models.TextField(verbose_name="میزان ترکیبات")
    who_to_use = models.TextField(verbose_name="طریقه مصرف")
    complications_of_compounds = models.TextField(verbose_name="عوارض ترکیبات")
    prescription_complications = models.TextField(verbose_name="عوارض کلی نسخه")
    version_reference = models.TextField(verbose_name="مرجع نسخه")

    class Meta:
        verbose_name = "دانشنامه نسخ درمانی"
        verbose_name_plural = "دانشنامه نسخ درمانی"

    def __str__(self):
        return self.name


class EncyclopediaCombinedDrugs(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        REPORT = 1
        FAILED = 2
        ACCEPT = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)

    name = models.CharField(max_length=100, verbose_name="عنوان", unique=True)
    classification = models.CharField(max_length=100, verbose_name="طبقه بندی")
    latin_name = models.CharField(max_length=100, verbose_name="نام لاتین")
    # جوی
    bomi = models.TextField(verbose_name='بومی')
    created_at = models.DateTimeField(auto_now_add=True)
    compounds = models.TextField(verbose_name='ترکیبات')
    amount_of_compounds = models.TextField(verbose_name='مقدار ترکیبات')
    indications = models.TextField(verbose_name='موارد مصرف')
    prohibited_usage = models.TextField(verbose_name='موارد منع مصرف')
    complications = models.TextField(verbose_name='عوارض')
    pregnancy = models.TextField(verbose_name='بارداری')
    method_of_drug_production = models.TextField(verbose_name='روش تولید دارو')
    how_to_use = models.TextField(verbose_name='طریقه مصرف')
    treatment_duration = models.TextField(verbose_name='طول درمان')
    pharmaceutical_supplements = models.TextField(verbose_name='مکمل های دارویی')
    the_nature_of_the_drug = models.CharField(max_length=50, verbose_name='طبیعت دارو')
    drug_manufacturing_company = models.TextField(verbose_name='شرکت تولید کننده دارو')

    # articles = models.TextField(verbose_name='مقالات')

    class Meta:
        verbose_name = "دانشنامه داروهای ترکیبی"
        verbose_name_plural = "دانشنامه داروهای ترکیبی"

    def __str__(self):
        return self.name


class EncyclopediaCombinedDrugsArticle(models.Model):
    encyclopedia = models.ForeignKey(EncyclopediaCombinedDrugs, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleEncyclopedia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"


class EncyclopediaCombinedDrugsImage(models.Model):
    encyclopedia = models.ForeignKey(EncyclopediaCombinedDrugs, on_delete=SET_NULL, null=True)
    image = models.FileField(upload_to="EncyclopediaCombinedDrugs/",
                             validators=[FileExtensionValidator(['jpg', 'png', 'svg', 'jpeg'])])

    class Meta:
        verbose_name = "تصاویر داروهای ترکیبی"
        verbose_name_plural = "تصاویر داروهای ترکیبی"

    def __str__(self):
        return self.encyclopedia.name


class HerbalEncyclopedia(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        REPORT = 1
        FAILED = 2
        ACCEPT = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)

    name = models.CharField(max_length=50, verbose_name='نام', unique=True)
    another_name = models.CharField(max_length=50, verbose_name='نام دیگر', unique=True)
    latin_name = models.CharField(max_length=54, verbose_name='نام لاتین', unique=True)
    habitat = models.CharField(max_length=40, verbose_name='زیستگاه')
    history = models.CharField(max_length=50, verbose_name='تاریخه', unique=True)
    components = models.TextField(verbose_name='اجزاء')
    compounds = models.TextField(verbose_name='ترکیبات')
    pharmacology = models.TextField(verbose_name='داروشناسی')
    indications = models.TextField(verbose_name='نشانه ها')
    effects = models.TextField(verbose_name='اثرات')
    the_nature_of_the_plant = models.TextField(verbose_name='طبیعت گیاه')
    complications = models.TextField(verbose_name='عوارض')
    pregnancy = models.TextField(verbose_name='بارداری')
    treatment_duration = models.TextField(verbose_name='درمان مدت')
    lifespan_of_the_plant = models.TextField(verbose_name='طول عمر گیاه')
    prohibited_usage = models.TextField(verbose_name='استفاده ممنوع')
    supplements = models.TextField(verbose_name='مکمل')
    maintenance_method = models.TextField(verbose_name='نگهداری روش')
    plant_structure = models.TextField(verbose_name='گیاه ساختار')
    plant_type = models.TextField(verbose_name='گیاه نوع')
    dosage = models.TextField(verbose_name='مقدار مصرف')
    how_to_use = models.TextField(verbose_name='نحوه استفاده')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'دایره المعارف گیاهی'
        verbose_name_plural = 'دایره المعارف های گیاهی'


class HerbalEncyclopediaArticle(models.Model):
    herbal = models.ForeignKey(HerbalEncyclopedia, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleEncyclopedia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"


class HerbalEncyclopediaReference(models.Model):
    refrence = models.ForeignKey(ArticleReference, on_delete=models.CASCADE)
    herbal = models.ForeignKey(HerbalEncyclopedia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ارجاع'
        verbose_name_plural = 'ارجاعات'


class HerbalEncyclopediaImage(models.Model):
    image = models.FileField(upload_to="herbal-encycloperdia",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'svg'])], verbose_name='تصویر')
    ref = models.ForeignKey('HerbalEncyclopedia', on_delete=CASCADE)

    class Meta:
        verbose_name = 'تصویر'
        verbose_name_plural = 'تصاویر'


class EncyclopediaOfDiseases(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        REPORT = 1
        FAILED = 2
        ACCEPT = 3

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)

    name = models.CharField(max_length=50, verbose_name='نام', unique=True)
    another_name = models.CharField(max_length=50, verbose_name='نام دیگر', unique=True)
    latin_name = models.CharField(max_length=50, verbose_name='نام لاتین', unique=True)
    classification = models.CharField(max_length=50, verbose_name='دسته بندی')
    native = models.CharField(max_length=50, verbose_name='زیست بوم')
    history = models.CharField(max_length=50, verbose_name='تاریخچه')
    the_structure_of_the_disease = models.CharField(max_length=50, verbose_name='ساختار بیماری')
    cause_of_illness = models.CharField(max_length=50, verbose_name='علت بیماری')
    disease_factors = models.CharField(max_length=50, verbose_name='عوامل بیماری')
    course_of_illness = models.CharField(max_length=50, verbose_name='دوره بیماری')
    treatment_methods = models.CharField(max_length=50, verbose_name='روش های درمان')
    treatment_duration = models.CharField(max_length=50, verbose_name='درمان مدت')
    coping_method = models.CharField(max_length=50, verbose_name='روش مقابله')
    disease_prevention = models.CharField(max_length=50, verbose_name='پیشگیری از بیماری')
    cases_of_exacerbation_of_the_disease = models.CharField(max_length=50, verbose_name='موارد تشدید بیماری')
    pregnancy = models.TextField(verbose_name='بارداری')
    hereditary_history = models.TextField(verbose_name='سابقه وراثتی')
    type_of_disease = models.TextField(verbose_name='نوع بیماری')
    phase_description_from_start_to_finish = models.TextField(verbose_name='توضیجات فاز شروع تا پایان بیماری')
    created_at = models.DateTimeField(auto_now_add=True)  # این خط را اضافه کن

    class Meta:
        verbose_name = 'دایره المعارف بیماری '
        verbose_name_plural = 'دایره المعارف بیماری ها'


class EncyclopediaOfDiseasesArticle(models.Model):
    encyclopedia = models.ForeignKey(EncyclopediaOfDiseases, on_delete=models.CASCADE)
    article = models.ForeignKey(ArticleEncyclopedia, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "مقاله بیماری"
        verbose_name_plural = "مقالات بیماری"


class EncyclopediaOfDiseasesReference(models.Model):
    refrence = models.ForeignKey(ArticleReference, on_delete=models.CASCADE)
    herbal = models.ForeignKey(EncyclopediaOfDiseases, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'ارجاع'
        verbose_name_plural = 'ارجاعات'


class EncyclopediaOfDiseasesImage(models.Model):
    image = models.FileField(upload_to="encyclopedia-of-diseases",
                             validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'svg'])], verbose_name='تصاویر')
    ref = models.ForeignKey('EncyclopediaOfDiseases', on_delete=CASCADE)


# news
from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان خبر")
    content = RichTextField(verbose_name="متن خبر")
    excerpt = models.TextField(verbose_name="خلاصه خبر")
    image = models.ImageField(upload_to='news_images/', verbose_name="تصویر")
    hashtags = models.ManyToManyField('Hashtag', related_name='news', verbose_name="هشتگ‌ها")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")

    class Meta:
        verbose_name = "خبر"
        verbose_name_plural = "اخبار"

    def __str__(self):
        return self.title


class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="نام هشتگ")

    class Meta:
        verbose_name = "هشتگ"
        verbose_name_plural = "هشتگ‌ها"

    def __str__(self):
        return self.name

class Comment(models.Model):
    COMMENT_STATUS_CHOICES = [
        ('active', 'فعال'),
        ('inactive', 'غیرفعال'),
        ('recomment', 'پاسخ'),
    ]

    news = models.ForeignKey(News, related_name='comments', on_delete=models.CASCADE, verbose_name="خبر")
    user_name = models.CharField(max_length=100, verbose_name="نام کاربر")
    email = models.EmailField(verbose_name="ایمیل")
    message = models.TextField(verbose_name="پیام")
    status = models.CharField(max_length=10, choices=COMMENT_STATUS_CHOICES, default='active', verbose_name="وضعیت")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")
    parent_comment = models.ForeignKey('self', related_name='recomments', null=True, blank=True,
                                       on_delete=models.CASCADE, verbose_name="پاسخ به")

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"نظر توسط {self.user_name} درباره {self.news.title}"