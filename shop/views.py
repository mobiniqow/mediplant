from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from jdatetime import timedelta
from rest_framework import generics, status, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import math
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, get_object_or_404

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import User
from sale.models import SaleBasket
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from .filter.product_filter import ShopProductFilter
from .models import ShopProduct, Shop, ProductNeedToAdded, ShopSettlement
from .serializers import ShopProductSerializer, ShopSerializers, ShopLoginSerializer, ShopProductCreateSerializer, \
    ShopProductUpdateSerializer, ProductNeedToAddedSerializer, UserShopProfileUpdateSerializer, \
    ChangePasswordSerializer, ShopSettlementSerializer, SaleBasketSerializer, SaleBasketStateUpdateSerializer


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
        user = self.request.user
        my_shops = Shop.objects.filter(user=user)
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


class ShopTransactionsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop, user=self.request.user)
        return Transaction.objects.filter(cart__shop=shop)


class ShopSettlementRequestAPIView(generics.CreateAPIView, generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShopSettlementSerializer

    def get_queryset(self):
        shop = get_object_or_404(Shop, user=self.request.user)
        return ShopSettlement.objects.filter(shop=shop)


class ShopSaleBasketListAPIView(generics.ListAPIView):
    serializer_class = SaleBasketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        shop = get_object_or_404(Shop, user=self.request.user)
        return SaleBasket.objects.filter(shop=shop).order_by('-created_at')


class ShopSaleBasketStateUpdateAPIView(generics.UpdateAPIView):
    serializer_class = SaleBasketStateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        shop = get_object_or_404(Shop, user=self.request.user)
        basket = get_object_or_404(SaleBasket, id=self.kwargs['pk'], shop=shop)
        return basket


class ShopSalesStatisticsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        shop = get_object_or_404(Shop, user=request.user)
        filter_type = request.query_params.get("filter", "daily")  # مقدار پیش‌فرض: روزانه

        today = now().date()
        if filter_type == "daily":
            start_date = today
        elif filter_type == "weekly":
            start_date = today - timedelta(days=7)
        elif filter_type == "monthly":
            start_date = today - timedelta(days=30)
        else:
            return Response({"error": "نوع فیلتر معتبر نیست. از daily, weekly یا monthly استفاده کنید."}, status=400)

        sales = SaleBasket.objects.filter(
            shop=shop,
            created_at__date__gte=start_date,
            state=SaleBasket.State.DONE_AND_FINISH  # فقط سبدهای تکمیل‌شده محاسبه شوند
        )

        total_sales = sales.count()
        total_income = sum(sale.price - sale.discount for sale in sales)

        return Response({
            "total_sales": total_sales,
            "total_income": total_income,
            "filter": filter_type
        })


class IsShopper(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == User.Role.SHOPPER


class ShopDetailView(APIView):
    """API برای دریافت و به‌روزرسانی اطلاعات فروشگاه"""
    permission_classes = [permissions.IsAuthenticated, IsShopper]

    def get(self, request):
        """دریافت اطلاعات فروشگاه کاربر"""
        shop = get_object_or_404(Shop, user=request.user)
        serializer = UserShopProfileUpdateSerializer(shop)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        """به‌روزرسانی اطلاعات فروشگاه"""
        shop = get_object_or_404(Shop, user=request.user)
        serializer = UserShopProfileUpdateSerializer(shop, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)