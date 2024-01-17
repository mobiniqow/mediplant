from django.urls import path

from  .views import ProductAPIView

urlpatterns = [
    path('filter', ProductAPIView.as_view())
]
