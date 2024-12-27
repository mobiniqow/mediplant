from django.contrib import admin
from .models import SaleBasket, SaleBasketProduct


class SaleBasketProductInline(admin.TabularInline):
    model = SaleBasketProduct
    extra = 0


@admin.register(SaleBasket)
class SaleBasketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'price', 'address', 'state', 'discount', 'shop', 'transaction']
    list_filter = ['state', 'created_at']
    search_fields = ['user__username', 'shop__name']
    list_per_page = 20
    inlines = [SaleBasketProductInline]

    class Meta:
        model = SaleBasket
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد‌های خرید'


@admin.register(SaleBasketProduct)
class SaleBasketProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'basket', 'product', 'created_at', 'unit']
    search_fields = ['basket__id', 'product__name']
    list_per_page = 20

    class Meta:
        model = SaleBasketProduct
        verbose_name = 'محصول سبد خرید'
        verbose_name_plural = 'محصولات سبد خرید'
