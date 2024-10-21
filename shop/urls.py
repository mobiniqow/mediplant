from django.urls import path

from .views import ShopProductAPIView

urlpatterns = [
    path('api/v1/', ShopProductAPIView.as_view(), name='shop_product'),
]
