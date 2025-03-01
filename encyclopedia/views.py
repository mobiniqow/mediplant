from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from encyclopedia.models import EncyclopediaCombinedDrugs, ArticleEncyclopedia, EncyclopediaOfDiseases
from .serializers import EncyclopediaCombinedDrugsSerializer, ArticleEncyclopediaSerializer, \
    EncyclopediaOfDiseasesSerializer
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 20
class EncyclopediaCombinedDrugsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EncyclopediaCombinedDrugs.objects.all().order_by('-created_at')
    serializer_class = EncyclopediaCombinedDrugsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['classification', 'the_nature_of_the_drug', 'state']
    search_fields = ['name', 'latin_name', 'compounds']
    ordering_fields = ['created_at', 'name']
    pagination_class = CustomPagination


class ArticleEncyclopediaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ArticleEncyclopedia.objects.all().order_by('-created_at')
    serializer_class = ArticleEncyclopediaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # **فیلترگذاری بر اساس دسته‌بندی و نویسنده**
    filterset_fields = ['category', 'author']

    # **جستجو بر اساس عنوان و نویسنده**
    search_fields = ['name', 'author']

    # **مرتب‌سازی بر اساس تاریخ ایجاد و نام**
    ordering_fields = ['created_at', 'name']

    # **فعال‌سازی صفحه‌بندی**
    pagination_class = CustomPagination



class EncyclopediaOfDiseasesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EncyclopediaOfDiseases.objects.all().order_by('-created_at')
    serializer_class = EncyclopediaOfDiseasesSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # **فیلترگذاری**
    filterset_fields = ['classification', 'state']

    # **جستجو بر اساس نام و نام لاتین**
    search_fields = ['name', 'latin_name']

    # **مرتب‌سازی بر اساس تاریخ ایجاد و نام**
    ordering_fields = ['created_at', 'name']

    # **فعال‌سازی صفحه‌بندی**
    pagination_class = CustomPagination

