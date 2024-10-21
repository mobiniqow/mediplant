from django.urls import path

from  .views import ProductAPIView

urlpatterns = [
    path('api/', ProductAPIView.as_view())
]
