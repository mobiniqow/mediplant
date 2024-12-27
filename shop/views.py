from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

from .filter.product_filter import ShopProductFilter
from .models import ShopProduct
from .serializers import ShopProductSerializer


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
