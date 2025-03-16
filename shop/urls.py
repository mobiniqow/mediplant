from django.urls import path

from .views import ShopProductAPIView, ShopLoginView, MyShopProductsView, ShopProductCreateView, ShopProductUpdateView, \
    ShopProductDeleteView, ProductNeedToAddedCreateView, UserShopProfileUpdateView, ChangePasswordView, \
    ShopTransactionsAPIView, ShopSettlementRequestAPIView, ShopSaleBasketListAPIView, ShopSaleBasketStateUpdateAPIView, \
    ShopSalesStatisticsAPIView

urlpatterns = [
    path('api/v1/shop-product/', ShopProductAPIView.as_view(), name='shop_product'),
    path('api/v1/shops/', ShopProductAPIView.as_view(), name='shops'),
    path('login/', ShopLoginView.as_view(), name='shop-login'),
    path('products/', MyShopProductsView.as_view(), name='my-shop-products'),
    path('products/create/', ShopProductCreateView.as_view(), name='shop-product-create'),
    path('products/update/<int:pk>/', ShopProductUpdateView.as_view(), name='shop-product-update'),
    path('products/delete/<int:pk>/', ShopProductDeleteView.as_view(), name='shop-product-delete'),
    path('products/request/', ProductNeedToAddedCreateView.as_view(), name='product-need-to-add'),
    path('profile/update/', UserShopProfileUpdateView.as_view(), name='user-shop-profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('transactions/', ShopTransactionsAPIView.as_view(), name='shop-transactions'),
    path('settlements/', ShopSettlementRequestAPIView.as_view(), name='shop-settlement'),
    path('baskets/', ShopSaleBasketListAPIView.as_view(), name='shop-baskets-list'),
    path('baskets/<int:pk>/update-state/', ShopSaleBasketStateUpdateAPIView.as_view(),
         name='shop-basket-update-state'),
    path('sales-stats/', ShopSalesStatisticsAPIView.as_view(), name='shop-sales-stats'),

]
