from django.contrib import admin
from .models import ClassId, Product, ProductImage, ProductUnit, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ('image',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['trade_id', 'class_id', 'name', 'type', 'material', 'state', 'is_active']
    search_fields = ['trade_id', 'name']
    list_filter = ['class_id', 'type', 'material', 'state', 'is_active', 'category']
    list_per_page = 20
    inlines = [ProductImageInline, ]


@admin.register(ClassId)
class ClassIdAdmin(admin.ModelAdmin):
    list_display = ['name', ]
    search_fields = ['name', ]
    list_per_page = 20


@admin.register(ProductUnit)
class ProductUnitAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    list_per_page = 20
