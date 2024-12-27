from django.urls import path
from .views import ProductAPIView, ProductTypeListView, CategoryListView

urlpatterns = [
    path('api/', ProductAPIView.as_view()),
    path('product-types/', ProductTypeListView.as_view(), name='product-types'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
]
