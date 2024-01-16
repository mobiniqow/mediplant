from django.urls import path

from shop.views import ProductAPIView

urlpatterns = [
    path('filter', ProductAPIView.as_view())
]
