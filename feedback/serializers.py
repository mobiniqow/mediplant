from rest_framework import serializers
from feedback.models import FeedbackObject


class FeedbackObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackObject
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at', 'is_approved']
        read_only_fields = ['id', 'user', 'created_at', 'is_approved']

    def validate_rating(self, value):
        """مقدار امتیاز باید بین ۱ تا ۵ باشد."""
        if value < 1 or value > 5:
            raise serializers.ValidationError("امتیاز باید بین ۱ تا ۵ باشد.")
        return value


class FeedbackUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackObject
        fields = ['rating', 'comment']

    def validate(self, data):
        """بررسی اینکه آیا کاربر می‌تواند نظر را ویرایش کند یا نه"""
        instance = self.instance
        if instance.is_approved:
            raise serializers.ValidationError("این نظر قبلاً تأیید شده است و امکان ویرایش آن وجود ندارد.")
        return data


class ShopFeedbackListSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name')
    user_name = serializers.CharField(source='user.username')

    class Meta:
        model = FeedbackObject
        fields = ['id', 'product_name', 'user_name', 'rating', 'comment', 'created_at']


class FeedbackApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackObject
        fields = ['is_approved']

    def update(self, instance, validated_data):
        """فقط ادمین می‌تواند نظر را تأیید کند"""
        request = self.context.get('request')
        if not request.user.is_staff:
            raise serializers.ValidationError("شما اجازه این کار را ندارید.")

        instance.is_approved = validated_data.get('is_approved', instance.is_approved)
        instance.save()
        return instance
