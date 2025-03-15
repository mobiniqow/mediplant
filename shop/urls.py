from django.urls import path

from .views import ShopProductAPIView, ShopLoginView, MyShopProductsView, ShopProductCreateView, ShopProductUpdateView, \
    ShopProductDeleteView, ProductNeedToAddedCreateView, UserShopProfileUpdateView, ChangePasswordView

urlpatterns = [
    path('api/v1/shop-product/', ShopProductAPIView.as_view(), name='shop_product'),
    path('api/v1/shops/', ShopProductAPIView.as_view(), name='shops'),
    path('shop/login/', ShopLoginView.as_view(), name='shop-login'),
    path('products/', MyShopProductsView.as_view(), name='my-shop-products'),
    path('products/create/', ShopProductCreateView.as_view(), name='shop-product-create'),
    path('products/update/<int:pk>/', ShopProductUpdateView.as_view(), name='shop-product-update'),
    path('products/delete/<int:pk>/', ShopProductDeleteView.as_view(), name='shop-product-delete'),
    path('products/request/', ProductNeedToAddedCreateView.as_view(), name='product-need-to-add'),
    path('profile/update/', UserShopProfileUpdateView.as_view(), name='user-shop-profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),

]

