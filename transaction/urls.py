from django.urls import path
from . import views
from .doctor_view import start_doctor_payment,  generate_doctor_payment_token

urlpatterns = [
    path('transactions/', views.ListTransactions.as_view(), name='list_transactions'),
    path('payment/start/', views.start_payment, name='start_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('payment/transactions/', views.get_transactions, name='get_transactions'),
    path('payment/url/', views.get_payment_url, name='get_payment_url'),
    # start-doctor-payment
    path('doctor/payment/start/', start_doctor_payment, name='start_doctor_payment'),
    # path('doctor/payment/verify/', verify_doctor_payment, name='verify_doctor_payment'),
    path('doctor/payment/token/', generate_doctor_payment_token, name='generate_doctor_payment_token'),

]
