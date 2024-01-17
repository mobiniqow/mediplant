from django.shortcuts import render
from rest_framework.views import APIView
from  .filter.product_filter import ProductFilter
from django_filters import rest_framework as filters
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializers


class ProductAPIView(generics.ListAPIView):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    ordering_fields = ['name', 'price']
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
