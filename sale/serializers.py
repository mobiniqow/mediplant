from rest_framework import serializers

from .models import SaleBasketProduct


class BaseProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleBasketProduct
        fields = '__all__'
