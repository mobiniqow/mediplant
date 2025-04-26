from django.contrib import admin
from .models import TraditionalMedicineDisease

@admin.register(TraditionalMedicineDisease)
class TraditionalMedicineDiseaseAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20

    class Meta:
        model = TraditionalMedicineDisease
        verbose_name = 'بیماری طب سنتی'
        verbose_name_plural = 'بیماری‌های طب سنتی'