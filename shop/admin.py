from itertools import product

from django.contrib import admin
from .models import Shop, ShopImage, ShopPhone, ShopProduct, CertificateImage, ProductNeedToAdded


class ShopPhoneInline(admin.TabularInline):
    model = ShopPhone
    fields = ('phone',)


class ShopImageInline(admin.TabularInline):
    model = ShopImage
    fields = ('image',)


class CertificateImageInline(admin.TabularInline):
    model = CertificateImage
    fields = ('certificate_image',)


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'trade_id', 'state', 'user']
    search_fields = ['name', 'trade_id', 'user__username']
    list_filter = ['state']
    inlines = [ShopPhoneInline, ShopImageInline, CertificateImageInline]
    list_per_page = 20

    class Meta:
        model = Shop


@admin.register(ShopImage)
class ShopImageAdmin(admin.ModelAdmin):
    list_display = ['shop', 'image']
    search_fields = ['shop__name']
    list_per_page = 20

    class Meta:
        model = ShopImage


@admin.register(ShopPhone)
class ShopPhoneAdmin(admin.ModelAdmin):
    list_display = ['shop', 'phone']
    search_fields = ['shop__name']
    list_per_page = 20

    class Meta:
        model = ShopPhone


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ['shop', 'product', 'created_at', 'updated_at', 'capacity', 'inventory_state', 'price']
    search_fields = ['shop__name', 'product__name','id']
    list_filter = ['inventory_state','shop']
    list_per_page = 20

    class Meta:
        model = ShopProduct

@admin.register(ProductNeedToAdded)
class ProductNeedToAddedAdmin(admin.ModelAdmin):
    list_display = [ 'name','description','shop',]
    search_fields = ['shop__name', 'id']
    list_filter = [ 'shop']
    list_per_page = 20

    class Meta:
        model = ShopProduct
