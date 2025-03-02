from rest_framework import viewsets, filters, generics
from django_filters.rest_framework import DjangoFilterBackend
from encyclopedia.models import EncyclopediaCombinedDrugs, ArticleEncyclopedia, EncyclopediaOfDiseases, \
    HerbalEncyclopedia, News, Comment
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import EncyclopediaCombinedDrugsSerializer, ArticleEncyclopediaSerializer, \
    EncyclopediaOfDiseasesSerializer, HerbalEncyclopediaSerializer, NewsListSerializer, NewsSerializer, \
    CommentSerializer
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


class HerbalEncyclopediaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = HerbalEncyclopedia.objects.all().order_by('-created_at')
    serializer_class = HerbalEncyclopediaSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['state']
    search_fields = ['name', 'latin_name', 'another_name']
    ordering_fields = ['created_at', 'name']
    pagination_class = CustomPagination


# news
class NewsListView(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # اینجا می‌توانید فیلترها را اضافه کنید
        queryset = super().get_queryset()
        return queryset


class NewsDetailView(generics.RetrieveAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CommentListView(generics.ListAPIView,generics.CreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        news_id = self.kwargs['news_id']
        status_filter = self.request.query_params.get('status', 'active')  # فیلتر وضعیت کامنت‌ها
        return Comment.objects.filter(news_id=news_id, status=status_filter)


    def perform_create(self, serializer):
        news_id = self.kwargs['news_id']
        serializer.save(news_id=news_id)

@api_view(['GET'])
def get_comment_count(request, news_id):
    comment_count = Comment.objects.filter(news_id=news_id, status='active').count()
    return Response({'comment_count': comment_count})

