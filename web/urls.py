from django.urls import path

from sale.views import Checkout
from .views.articles import BlogsView, BlogsDetailsView
from .views.auth import LoginView, VerifyView, ProfileView
from .views.others import AboutUsView, ContactUsView
from .views.product import ShopProductListView, ShopProductView, ProductListView
from .views.shop import CategoryView, IndexView, ShopView, ShopDetailsView, SearchProduct, CheckoutView, ShopCartView

urlpatterns = [
    path("", IndexView.as_view(),),
    path("search/", CategoryView.as_view(),),
    path("product/", ProductListView.as_view(),),
    path("search/product/<int:product_id>/", SearchProduct.as_view(),),
    path("about-us", AboutUsView.as_view(),),
    path("contact-us", ContactUsView.as_view(),),
    path("blog", BlogsView.as_view(),),
    path("blog/<int:id>/", BlogsDetailsView.as_view(),),
    path('shop/', ShopView.as_view()),
    path('shop/<int:id>/', ShopDetailsView.as_view()),
    path('shop/<int:id>/cart', ShopCartView.as_view()),
    path('shop/<int:id>/checkout', CheckoutView.as_view()),
    path('shop/<int:shop_id>/product/', ShopProductListView.as_view()),
    path('shop/<int:shop_id>/product/<int:product_id>/', ShopProductView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/<str:phone>/', VerifyView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view()),
]
