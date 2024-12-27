from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)
    formatted_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_image(self, obj):
        product = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(product, many=True).data

    def get_formatted_price(self, obj):
        return '{:,.0f}'.format(obj.price)

class ProductTypeSerializer(serializers.Serializer):
    value = serializers.IntegerField()
    label = serializers.CharField()

    def to_representation(self, instance):
        return {
            'value': instance[0],
            'label': instance[1]
        }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'image']
