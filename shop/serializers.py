from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from product.models import ProductImage, Product
from product.serializers import ProductImageSerializer
from sale.models import SaleBasket, SaleBasketProduct
from sale.serializers import BaseProductSerializer
from .models import ShopProduct, Shop, ProductNeedToAdded, ShopSettlement
from django.contrib.auth import authenticate
from account.models import User


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


class ShopLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        # بررسی صحت اطلاعات کاربری
        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("شماره تلفن یا رمز عبور اشتباه است.")

        print(user.role)
        if user.role != User.Role.SHOPPER:
            raise serializers.ValidationError("این حساب کاربری فروشنده نیست.")

        data['user'] = user
        return data


class ShopProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['product', 'capacity', 'inventory_state', 'price', 'material', 'how_to_use']

    def create(self, validated_data):
        user = self.context['request'].user  # دریافت کاربر لاگین‌شده
        shop = Shop.objects.filter(user=user).first()  # دریافت فروشگاه متعلق به کاربر

        if not shop:
            raise serializers.ValidationError({"error": "شما فروشگاهی ندارید."})

        validated_data['shop'] = shop  # تنظیم فروشگاه
        return super().create(validated_data)


class ShopProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopProduct
        fields = ['capacity', 'inventory_state', 'price', 'material', 'how_to_use']

    def update(self, instance, validated_data):
        user = self.context['request'].user  # دریافت کاربر لاگین‌شده
        if instance.shop.user != user:  # بررسی مالکیت فروشگاه
            raise serializers.ValidationError({"error": "شما مجاز به ویرایش این محصول نیستید."})

        return super().update(instance, validated_data)


class ProductNeedToAddedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductNeedToAdded
        fields = ['id', 'name', 'image', 'description']

    def create(self, validated_data):
        user = self.context['request'].user

        # بررسی اینکه کاربر مالک یک فروشگاه است
        shop = user.shop_set.first()
        if not shop:
            raise serializers.ValidationError({"error": "شما فروشگاهی ندارید."})

        # ایجاد محصول جدید برای اضافه شدن
        validated_data['shop'] = shop
        return super().create(validated_data)


class ShopSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopSettlement
        fields = '__all__'
        read_only_fields = ['status', 'shop', 'created_at', 'receipt_image', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        shop = get_object_or_404(Shop, user=user)
        validated_data['shop'] = shop
        return super().create(validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        # دریافت پسوردهای قدیمی و جدید
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        # بررسی اینکه پسورد جدید و تاییدیه با هم مطابقت داشته باشند
        if new_password != confirm_password:
            raise serializers.ValidationError("پسورد جدید و تاییدیه پسورد جدید با هم مطابقت ندارند.")

        # بررسی اینکه پسورد قدیمی صحیح باشد
        user = self.context['request'].user  # کاربر احراز هویت شده
        if not user.check_password(old_password):
            raise serializers.ValidationError("پسورد قدیمی صحیح نیست.")

        return attrs

    def update(self, instance, validated_data):
        # آپدیت پسورد کاربر
        new_password = validated_data['new_password']
        instance.set_password(new_password)  # تغییر پسورد
        instance.save()  # ذخیره تغییرات
        return instance


class SaleBasketSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SaleBasket
        fields = ['id', 'user', 'price', 'state', 'created_at', 'delivery_date', 'items', ]

    def get_items(self, obj):
        basket = obj
        items = SaleBasketProduct.objects.filter(basket=basket)
        return BaseProductSerializer(items, many=True).data


class SaleBasketStateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleBasket
        fields = ['state']

    def validate_state(self, value):
        basket = self.instance
        if basket.state == SaleBasket.State.SHOP_CANCEL:
            raise serializers.ValidationError("این سبد قبلاً لغو شده و دیگر قابل تغییر نیست.")

        if value not in [SaleBasket.State.IN_SHOP_COMPILATION, SaleBasket.State.SENDING, SaleBasket.State.SHOP_CANCEL]:
            raise serializers.ValidationError(
                "فقط می‌توانید وضعیت را به IN_SHOP_COMPILATION، SENDING یا SHOP_CANCEL تغییر دهید.")

        return value


class UserShopProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"
        read_only_fields = ['user']  # کاربر را نمی‌توان از اینجا تغییر داد
