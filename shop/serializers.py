from rest_framework import serializers

from product.models import ProductImage, Product
from product.serializers import ProductImageSerializer
from .models import ShopProduct, Shop


class ShopProductSerializer(serializers.ModelSerializer):
    formatted_price = serializers.SerializerMethodField(read_only=True)
    images = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    type = serializers.SerializerMethodField(read_only=True)
    shop_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ShopProduct
        fields = '__all__'

    def get_formatted_price(self, obj):
        return '{:,.0f}'.format(obj.price)

    def get_shop_name(self, obj):
        return obj.shop.name

    def get_images(self, obj: ShopProduct):
        images = ProductImage.objects.filter(product=obj.product)
        return ProductImageSerializer(images, many=True).data

    def get_name(self, obj):
        return obj.product.name

    def get_description(self, obj):
        return obj.product.description

    def get_type(self, obj):
        return Product.Type(obj.product.type).label


class ShopSerializers(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
