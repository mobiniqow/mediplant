from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
# from django.contrib.gis.geos import Point
# from django.contrib.gis.db.models import Distance
import math
from django.contrib.gis.measure import D
from .filter.product_filter import ShopProductFilter
from .models import ShopProduct, Shop
from .serializers import ShopProductSerializer, ShopSerializers


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
