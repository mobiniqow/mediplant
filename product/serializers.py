from rest_framework import serializers

from product.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = "__all__"


class ProductSerializers(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    def get_image(self, obj):
        product = ProductImage.objects.filter(product=obj)
        return ProductImageSerializer(product, many=True).data
