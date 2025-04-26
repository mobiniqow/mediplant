from itertools import product

from django.contrib import admin
from django.db.models import Sum

from .models import Shop, ShopProduct, ProductNeedToAdded, ShopSettlement


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'trade_id', 'state', 'user']
    search_fields = ['name', 'trade_id', 'user__username']
    list_filter = ['state']
    list_per_page = 20

    class Meta:
        model = Shop


@admin.register(ShopProduct)
class ShopProductAdmin(admin.ModelAdmin):
    list_display = ['shop', 'product', 'created_at', 'updated_at', 'capacity', 'inventory_state', 'price']
    search_fields = ['shop__name', 'product__name', 'id']
    list_filter = ['inventory_state', 'shop']
    list_per_page = 20

    class Meta:
        model = ShopProduct


@admin.register(ProductNeedToAdded)
class ProductNeedToAddedAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'shop', ]
    search_fields = ['shop__name', 'id']
    list_filter = ['shop']
    list_per_page = 20

    class Meta:
        model = ShopProduct


class ShopSettlementAdmin(admin.ModelAdmin):
    list_display = ('shop', 'total_sales', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('shop__name', 'transaction_id')
    readonly_fields = ('total_sales',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            total_sales=Sum('shop__shopproduct__price')
        )
        return queryset

    def total_sales(self, obj):
        return obj.total_sales if hasattr(obj, 'total_sales') else 0

    total_sales.short_description = "مجموع فروش"


admin.site.register(ShopSettlement, ShopSettlementAdmin)
