from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from account.models import User
from .models import Doctor, DockterBranch, DoctorSettlement
from django.contrib.auth import authenticate


class DoctorSerializer(serializers.ModelSerializer):
    branch_name = serializers.CharField(source='branch.name', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'user', 'branch', 'branch_name', 'address', 'state',
            'picture', 'description', 'id_active', 'register_time',
            'responsiveness', 'postal_code', 'shaba'
        ]

class DockterBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockterBranch
        fields = '__all__'

class DoctorLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=17)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        phone = data.get('phone')
        password = data.get('password')

        # بررسی صحت اطلاعات کاربری
        user = authenticate(phone=phone, password=password)
        if not user:
            raise serializers.ValidationError("شماره تلفن یا رمز عبور اشتباه است.")

        if user.role != User.Role.DOCTOR:
            raise serializers.ValidationError("این حساب کاربری فروشنده نیست.")

        data['user'] = user
        return data

class DoctorSettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSettlement
        fields = '__all__'
        read_only_fields = ['status', 'doctor', 'created_at', 'receipt_image', 'updated_at']

    def create(self, validated_data):
        user = self.context['request'].user
        doctor = get_object_or_404(Doctor, user=user)
        validated_data['doctor'] = doctor
        return super().create(validated_data)

class DoctorShopProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"
        read_only_fields = ['user']  # کاربر را نمی‌توان از اینجا تغییر داد
