from django.urls import path

from .views.articles import BlogsView, BlogsDetailsView
from .views.others import AboutUsView, ContactUsView
from .views.shop import CategoryView, IndexView, ShopView, ShopDetailsView

urlpatterns = [
    path("", IndexView.as_view(), ),
    path("search/", CategoryView.as_view(), ),
    path("about-us", AboutUsView.as_view(), ),
    path("contact-us", ContactUsView.as_view(), ),
    path("blog", BlogsView.as_view(), ),
    path("blog/<int:id>/", BlogsDetailsView.as_view(), ),
    path('shop/', ShopView.as_view()),
    path('shop/<int:id>/', ShopDetailsView.as_view()),
]
