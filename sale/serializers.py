from rest_framework import serializers

from product.models import ProductImage
from shop.models import ShopProduct
from .models import SaleBasketProduct, SaleBasket


class BaseProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    type = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()
    class Meta:
        model = SaleBasketProduct
        fields = '__all__'

    def get_image(self, obj:SaleBasketProduct):
        product = obj.product.product
        image = ProductImage.objects.filter(product=product)
        if image.exists():
            image = image[0]
            return image.image.url
        else:
            # todo default image
            pass

    def get_name(self, obj:SaleBasketProduct):
        product = obj.product.product
        name = product.name
        return name
    def get_type(self, obj:SaleBasketProduct):
        product = obj.product
        type = product.get_material_display()
        return type
    def get_price(self, obj:SaleBasketProduct):
        product = obj.product
        price = product.price
        return price

class BasketSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    class Meta:
        model = SaleBasket
        fields = '__all__'

    def get_image(self, obj:SaleBasket):
        return obj.shop.image.url
    def get_name(self, obj:SaleBasket):
        return obj.shop.name