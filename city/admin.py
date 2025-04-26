from django.contrib import admin
from .models import Country, City, CityLocation


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20

    class Meta:
        model = Country


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    search_fields = ['name', 'country__name']
    list_filter = ['country']
    list_per_page = 20

    class Meta:
        model = City


@admin.register(CityLocation)
class CityLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']
    list_filter = ['city__name']
    search_fields = ['name', 'city__name']
    list_per_page = 20

    class Meta:
        model = CityLocation
