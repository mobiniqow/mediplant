from rest_framework import serializers

from sale.models import SaleBasketProduct
from sale.serializers import BaseProductSerializer
from transaction.models import Transaction


# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    # shop_name = serializers.CharField(source='cart.shop.name', read_only=True)
    date_shamsi = serializers.CharField(source='get_shamsi_date', read_only=True)
    items_count = serializers.IntegerField(source='cart.salebasketproduct_set.count', read_only=True)
    items = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Transaction
        fields = ['date_shamsi','amount', 'items_count', 'items', 'status']

    def get_items(self, obj):
        if not obj.cart:
            return []
        items = obj.cart.salebasketproduct_set.filter(product__isnull=False)
        return BaseProductSerializer(items, many=True).data



