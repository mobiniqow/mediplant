from django.contrib import admin
from .models import Shop, ShopImage, ShopPhone, ShopProduct


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'trade_id', 'state', 'user']
    search_fields = ['name', 'trade_id', 'user__username']
    list_filter = ['state']
    list_per_page = 20

    class Meta:
        model = Shop


@admin.register(ShopImage)
class ShopImageAdmin(admin.ModelAdmin):
    list_display = ['shop', 'certificate_image']
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
    search_fields = ['shop__name', 'product__name']
    list_filter = ['inventory_state']
    list_per_page = 20

    class Meta:
        model = ShopProduct
