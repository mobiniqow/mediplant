from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ShopProductAPIView, ShopLoginView, MyShopProductsView, ShopProductCreateView, ShopProductUpdateView, \
    ShopProductDeleteView, ProductNeedToAddedCreateView, ChangePasswordView, \
    ShopTransactionsAPIView, ShopSettlementRequestAPIView, ShopSaleBasketListAPIView, ShopSaleBasketStateUpdateAPIView, \
    ShopSalesStatisticsAPIView,  ShopDetailView

urlpatterns = [
    path('profile/', ShopDetailView.as_view(), name='shop_detail'),
    path('api/v1/shop-product/', ShopProductAPIView.as_view(), name='shop_product'),
    path('api/v1/shops/', ShopProductAPIView.as_view(), name='shops'),
    path('login/', ShopLoginView.as_view(), name='shop-login'),
    path('products/', MyShopProductsView.as_view(), name='my-shop-products'),
    path('products/create/', ShopProductCreateView.as_view(), name='shop-product-create'),
    path('products/update/<int:pk>/', ShopProductUpdateView.as_view(), name='shop-product-update'),
    path('products/delete/<int:pk>/', ShopProductDeleteView.as_view(), name='shop-product-delete'),
    path('products/request/', ProductNeedToAddedCreateView.as_view(), name='product-need-to-add'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('transactions/', ShopTransactionsAPIView.as_view(), name='shop-transactions'),
    path('settlements/', ShopSettlementRequestAPIView.as_view(), name='shop-settlement'),
    path('baskets/', ShopSaleBasketListAPIView.as_view(), name='shop-baskets-list'),
    path('baskets/<int:pk>/update-state/', ShopSaleBasketStateUpdateAPIView.as_view(),
         name='shop-basket-update-state'),
    path('sales-stats/', ShopSalesStatisticsAPIView.as_view(), name='shop-sales-stats'),

]
