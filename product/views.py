from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from .filter.product_filter import ProductFilter
from .models import Product
from .serializers import ProductSerializers

class ProductPagination(PageNumberPagination):
    page_size = 9  # تعداد آیتم‌ها در هر صفحه

class ProductAPIView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price']
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = ProductPagination