from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import math
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from .filter.product_filter import ShopProductFilter
from .models import ShopProduct, Shop, ProductNeedToAdded
from .serializers import ShopProductSerializer, ShopSerializers, ShopLoginSerializer, ShopProductCreateSerializer, \
    ShopProductUpdateSerializer, ProductNeedToAddedSerializer, UserShopProfileUpdateSerializer, ChangePasswordSerializer


class ShopProductPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'total_pages': math.ceil(self.page.paginator.count / self.page_size),
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


class ShopProductAPIView(generics.ListAPIView):
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShopProductFilter
    pagination_class = ShopProductPagination


class ShopListView(generics.ListAPIView):
    serializer_class = ShopSerializers

    def get_queryset(self):
        user_lat = float(self.request.query_params.get('lat', 0))
        user_lng = float(self.request.query_params.get('lng', 0))

        # تبدیل مختصات ورودی به Point
        # user_location = Point(user_lng, user_lat, srid=4326)

        # جستجوی نزدیک‌ترین فروشگاه‌ها
        queryset = Shop.objects.all()
        # queryset = queryset.filter(location__distance_lte=(user_location, D(km=10)))  # فروشگاه‌های در 10 کیلومتر

        # مرتب‌سازی بر اساس نزدیک‌ترین فروشگاه‌ها
        # queryset = queryset.annotate(distance=Distance('location', user_location)).order_by('distance')

        return queryset


class ShopLoginView(APIView):
    def post(self, request):
        serializer = ShopLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyShopProductsView(ListAPIView):
    serializer_class = ShopProductSerializer

    def get_queryset(self):
        user = self.request.user  # دریافت کاربر لاگین‌شده
        my_shops = Shop.objects.filter(user=user)  # یافتن فروشگاه‌هایی که متعلق به این کاربر هستند
        return ShopProduct.objects.filter(shop__in=my_shops)

class ShopProductCreateView(CreateAPIView):
    serializer_class = ShopProductCreateSerializer
    permission_classes = [IsAuthenticated]  # فقط کاربران لاگین‌شده مجاز هستند

    def perform_create(self, serializer):
        serializer.save()  # ذخیره محصول جدید

class ShopProductUpdateView(UpdateAPIView):
    queryset = ShopProduct.objects.all()
    serializer_class = ShopProductUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user  # دریافت کاربر لاگین‌شده
        return ShopProduct.objects.filter(shop__user=user)


class ShopProductDeleteView(DestroyAPIView):
    queryset = ShopProduct.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product = self.get_object()

        # بررسی اینکه کاربر مالک این فروشگاه هست یا نه
        if product.shop.user != request.user:
            return Response({"error": "شما مجاز به حذف این محصول نیستید."}, status=status.HTTP_403_FORBIDDEN)

        product.delete()
        return Response({"message": "محصول با موفقیت حذف شد."}, status=status.HTTP_204_NO_CONTENT)

class ProductNeedToAddedCreateView(CreateAPIView):
    queryset = ProductNeedToAdded.objects.all()
    serializer_class = ProductNeedToAddedSerializer
    permission_classes = [IsAuthenticated]



class UserShopProfileUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserShopProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user  # برمی‌گرداند به کاربر احراز هویت شده


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # استفاده از Serializer برای تغییر پسورد
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            # ذخیره پسورد جدید
            serializer.update(request.user, serializer.validated_data)
            return Response({"detail": "پسورد با موفقیت تغییر یافت."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)