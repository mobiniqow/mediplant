from django.urls import path

from encyclopedia.views import BlogsAPIView

urlpatterns = [
    path('', BlogsAPIView.as_view()),
    # path('<int:id>', BlogsAPIView.as_view()),
]
