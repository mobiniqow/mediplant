from django.urls import path
from .views import CreateBasket, AddProductToBasket, UpdateProductUnit, RemoveProductFromBasket, Checkout, UpdateTransactionStatus

urlpatterns = [
    path('basket/create/', CreateBasket.as_view(), name='create_basket'),
    path('basket/<int:basket_id>/add_product/', AddProductToBasket.as_view(), name='add_product'),
    path('basket/<int:basket_id>/product/<int:product_id>/update/', UpdateProductUnit.as_view(), name='update_product_unit'),
    path('basket/<int:basket_id>/product/<int:product_id>/remove/', RemoveProductFromBasket.as_view(), name='remove_product'),
    path('basket/<int:basket_id>/checkout/', Checkout.as_view(), name='checkout'),
    path('transaction/<int:transaction_id>/update/', UpdateTransactionStatus.as_view(), name='update_transaction_status'),
]
