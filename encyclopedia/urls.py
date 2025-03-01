from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EncyclopediaCombinedDrugsViewSet, ArticleEncyclopediaViewSet, EncyclopediaOfDiseasesViewSet

router = DefaultRouter()
router.register(r'combined-drugs', EncyclopediaCombinedDrugsViewSet)
router.register(r'article-encyclopedia', ArticleEncyclopediaViewSet, basename='article-encyclopedia')
router.register(r'diseases', EncyclopediaOfDiseasesViewSet, basename='disease')
urlpatterns = [
    path('api/', include(router.urls)),
]
