from django.db import models


class TraditionalMedicineDisease(models.Model):
    name = models.CharField(max_length=255, verbose_name='نام بیماری',unique=True)
    description = models.TextField(verbose_name='توضیحات')
    causes = models.TextField(verbose_name='علل بیماری')
    symptoms = models.TextField(verbose_name='علائم بیماری')
    treatments = models.TextField(verbose_name='درمان‌های طب سنتی')
    prevention = models.TextField(verbose_name='پیشگیری از بیماری')

    class Meta:
        verbose_name = 'بیماری'
        verbose_name_plural = 'بیماری‌ها'

    def __str__(self):
        return self.name
