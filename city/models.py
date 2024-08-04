from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'کشور'
        verbose_name_plural = 'کشورها'


class City(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'شهر'
        verbose_name_plural = 'شهر ها'


class CityLocation(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'منطقه'
        verbose_name_plural = 'منطقه ها'
