from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'combined-drugs', views.EncyclopediaCombinedDrugsViewSet)
router.register(r'article-encyclopedia', views.ArticleEncyclopediaViewSet, basename='article-encyclopedia')
router.register(r'diseases', views.EncyclopediaOfDiseasesViewSet, basename='disease')
router.register(r'herbal-encyclopedia', views.HerbalEncyclopediaViewSet, basename='herbal')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/news/', views.NewsListView.as_view(), name='news-list'),
    path('api/news/<int:pk>/', views.NewsDetailView.as_view(), name='news-detail'),
    path('api/news/<int:news_id>/comments/', views.CommentListView.as_view(), name='comments'),
    path('api/news/<int:news_id>/comment_count/', views.get_comment_count, name='comment-count'),

]
