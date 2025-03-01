from django.urls import path

from .views.articles import EncyclopediaCombinedDrugsView, EncyclopediaCombinedDetailsView, EncyclopediaDetailsView, \
    EncyclopediaView, DiseasesView, DiseasesDetailsView
from .views.auth import LoginView, VerifyView, ProfileView
from .views.others import AboutUsView, ContactUsView
from .views.product import ShopProductListView, ShopProductView, ProductListView
from .views.shop import CategoryView, IndexView, ShopView, ShopDetailsView, SearchProduct, CheckoutView, ShopCartView, \
    OrderListView, CallbackView, ShopTransactions, AfterBankGateWay, ShopCartDetailsOrderView

urlpatterns = [
    path("", IndexView.as_view(), ),
    path("search/", CategoryView.as_view(), ),
    path("product/", ProductListView.as_view(), ),
    path("search/product/<int:product_id>/", SearchProduct.as_view(), ),
    path("about-us", AboutUsView.as_view(), ),
    path("contact-us", ContactUsView.as_view(), ),
    path('shops/', ShopView.as_view()),
    path('shop-transactions/', ShopTransactions.as_view()),
    path('callback/', CallbackView.as_view()),
    # path('shop/orders', OrderListView.as_view()),
    path('shop/<int:id>/', ShopDetailsView.as_view()),
    path('shop/<int:id>/cart', ShopCartView.as_view()),
    path('shop/<int:id>/checkout', CheckoutView.as_view()),
    path('shop/<int:shop_id>/product/', ShopProductListView.as_view()),
    path('shop/<int:shop_id>/product/<int:product_id>/', ShopProductView.as_view()),
    path('login/', LoginView.as_view()),
    path('verify/<str:phone>/', VerifyView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view()),
    path('track-order/<int:id>/', AfterBankGateWay.as_view()),
    path('track-order/<int:id>/items', ShopCartDetailsOrderView.as_view()),
#     blogs
    path("blog/encyclopedia-combined-drugs", EncyclopediaCombinedDrugsView.as_view(),),
    path("blog/encyclopedia-combined-drugs/<int:articleId>/", EncyclopediaCombinedDetailsView.as_view(),),
    path("blog/encyclopedia-article-encyclopedia", EncyclopediaView.as_view(),),
    path("blog/encyclopedia-article-encyclopedia/<int:articleId>/", EncyclopediaDetailsView.as_view(),),

    path("blog/encyclopedia-article-diseases/", DiseasesView.as_view(),),
    path("blog/encyclopedia-article-diseases/<int:articleId>/", DiseasesDetailsView.as_view(),),
]
