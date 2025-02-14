from django.urls import path
from .views import CreateDeleteBasket, ProductToBasket, Checkout, \
    UpdateTransactionStatus, MyBasket, DeleteProductFromBasket, CancelBasket

urlpatterns = [
    path('', MyBasket.as_view()),
    path('<int:shopid>', CreateDeleteBasket.as_view()),
    path('<int:shop_id>/remove/<int:product_id>', DeleteProductFromBasket.as_view()),
    path('<int:basket_id>/product/<int:product_id>', ProductToBasket.as_view(), name='product'),
    path('<int:basket_id>/checkout/', Checkout.as_view(), name='checkout'),
    path('transaction/<int:transaction_id>/update/', UpdateTransactionStatus.as_view(),
         name='update_transaction_status'),
    path('<int:basket_id>/', MyBasket.as_view()),
    path('cancel_cart/<int:basket_id>/', CancelBasket.as_view(), name='cancell_cart'),
]
