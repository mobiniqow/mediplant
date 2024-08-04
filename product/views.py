from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filter.product_filter import ProductFilter
from .models import Product
from .serializers import ProductSerializers


class ProductAPIView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price']
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
