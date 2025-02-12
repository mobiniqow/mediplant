from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.ListTransactions.as_view(), name='list_transactions'),
    path('payment/start/<int:shop_id>', views.start_payment, name='start_payment'),

    path('payment/verify/', views.verify_payment, name='verify_payment'),

    path('payment/transactions/', views.get_transactions, name='get_transactions'),

    path('payment/url/', views.get_payment_url, name='get_payment_url'),
]
