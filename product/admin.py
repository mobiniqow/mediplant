from django.contrib import admin
from .models import ClassId, Product, ProductImage, ProductUnit

@admin.register(ClassId)
class ClassIdAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20

    class Meta:
        model = ClassId


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['trade_id', 'class_id', 'name', 'type', 'material', 'state', 'is_active']
    search_fields = ['trade_id', 'name']
    list_filter = ['class_id', 'type', 'material', 'state', 'is_active']
    list_per_page = 20

    class Meta:
        model = Product


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image']
    search_fields = ['product__name']
    list_per_page = 20

    class Meta:
        model = ProductImage


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20

    class Meta:
        model = ProductUnit