from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
import math
from .filter.category_filter import CategoryFilter
from .filter.product_filter import ProductFilter, OrderingFilter
from .models import Product, Category
from .serializers import ProductSerializers, ProductTypeSerializer, CategorySerializer


class ProductPagination(PageNumberPagination):
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


class ProductAPIView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = ProductFilter
    ordering_fields = ['name',   'id','views']
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    pagination_class = ProductPagination
class ProductTypeListView(APIView):
    def get(self, request):
        product_types = Product.Type.choices
        serializer = ProductTypeSerializer(product_types, many=True)
        return Response(serializer.data)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CategoryFilter
    pagination_class = None