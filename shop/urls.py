from django.urls import path

from .views import ShopProductAPIView

urlpatterns = [
    path('api/v1/shop-product/', ShopProductAPIView.as_view(), name='shop_product'),
    path('api/v1/shops/', ShopProductAPIView.as_view(), name='shops'),

]
