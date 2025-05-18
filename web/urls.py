from django.urls import path

from encyclopedia.views import NewsDetailView
from .views.articles import EncyclopediaCombinedDrugsView, EncyclopediaCombinedDetailsView, EncyclopediaDetailsView, \
    EncyclopediaView, DiseasesView, DiseasesDetailsView, HerbalView, HerbalDetailsView, NewsView, NewsDetailsView
from .views.auth import LoginView, VerifyView, ProfileView,Tickets,NewTicket,TicketHistory
from .views.doctor import DoctorList, DoctorDetailsList, DoctorChatDetails, DoctorprescriptionDetails, \
    DoctorHistoryDetails, DoctorListDetails
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
    path('shop-transactions/', ShopTransactions.as_view()),
    path('callback/', CallbackView.as_view()),
    path("ticket/", Tickets.as_view(),),
    path("ticket/new", NewTicket.as_view(),),
    path("ticket/history", TicketHistory.as_view(),),
    # path('shop/orders', OrderListView.as_view()),
    path('shops/', ShopView.as_view()),
    path('shop/<int:id>/', ShopDetailsView.as_view()),
    path('shop/cart', ShopCartView.as_view()),
    path('shop/<int:id>/checkout', CheckoutView.as_view()),
    path('shop/<int:shop_id>/product/', ShopProductListView.as_view()),
    path('shop/<int:shop_id>/product/<int:product_id>/', ShopProductView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('verify/<str:phone>/', VerifyView.as_view(), name='verify'),
    path('profile/', ProfileView.as_view()),
    path('track-order/<int:id>/', AfterBankGateWay.as_view()),
    path('track-order/<int:id>/items', ShopCartDetailsOrderView.as_view()),
    #     blogs
    path("blog/encyclopedia-combined-drugs", EncyclopediaCombinedDrugsView.as_view(), ),
    path("blog/encyclopedia-combined-drugs/<int:articleId>/", EncyclopediaCombinedDetailsView.as_view(), ),
    path("blog/encyclopedia-article-encyclopedia", EncyclopediaView.as_view(), ),
    path("blog/encyclopedia-article-encyclopedia/<int:articleId>/", EncyclopediaDetailsView.as_view(), ),

    path("blog/encyclopedia-article-diseases/", DiseasesView.as_view(), ),
    path("blog/encyclopedia-article-diseases/<int:articleId>/", DiseasesDetailsView.as_view(), ),
    path("blog/encyclopedia-article-herbal/", HerbalView.as_view(), ),
    path("blog/encyclopedia-article-herbal/<int:articleId>/", HerbalDetailsView.as_view(), ),
    path("blog/news/", NewsView.as_view(),),
    path("blog/news/<int:articleId>/", NewsDetailsView.as_view(),),
    path("medicine/", DoctorList.as_view(),),
    path("medicine/<int:doctor>", DoctorDetailsList.as_view(),name="doctor-page"),
    path("medicine/<int:doctor>/chats/", DoctorChatDetails.as_view(),),
    path("medicine/<int:doctor>/prescription/", DoctorprescriptionDetails.as_view(),),
    path("medicine/prescription/", DoctorHistoryDetails.as_view(),),
    path("medicine/docktor-list/", DoctorListDetails.as_view(),),

]
