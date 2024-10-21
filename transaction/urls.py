from django.urls import path
from .views import InitiatePayment, ZarinpalCallback, CheckTransactionStatus

urlpatterns = [
    path('payment/initiate/<int:basket_id>/', InitiatePayment.as_view(), name='initiate_payment'),
    path('payment/callback/', ZarinpalCallback.as_view(), name='payment_callback'),
    path('payment/status/<int:transaction_id>/', CheckTransactionStatus.as_view(), name='check_transaction_status'),
]
