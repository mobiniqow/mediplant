from django.urls import path
from .views import CreateBasket, ProductToBasket, Checkout, \
    UpdateTransactionStatus

urlpatterns = [
    path('<int:shop_id>', CreateBasket.as_view(), name='create_basket'),
    path('<int:basket_id>/product/<int:product_id>', ProductToBasket.as_view(), name='product'),
    path('<int:basket_id>/checkout/', Checkout.as_view(), name='checkout'),
    path('transaction/<int:transaction_id>/update/', UpdateTransactionStatus.as_view(),
         name='update_transaction_status'),
]
