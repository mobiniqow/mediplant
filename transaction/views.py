import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings

from sale.models import SaleBasket
from .models import Transaction

ZARINPAL_MERCHANT_ID = 'your-merchant-id-here'
ZARINPAL_START_PAY_URL = 'https://www.zarinpal.com/pg/StartPay/{authority}'
ZARINPAL_REQUEST_URL = 'https://api.zarinpal.com/pg/v4/payment/request.json'
ZARINPAL_VERIFY_URL = 'https://api.zarinpal.com/pg/v4/payment/verify.json'


class InitiatePayment(APIView):
    def post(self, request, basket_id):
        basket = SaleBasket.objects.get(id=basket_id, user=request.user)

        if basket.price <= 0:
            return Response({"error": "Basket is empty"}, status=status.HTTP_400_BAD_REQUEST)
        transaction = Transaction.objects.create(
            price=basket.price,
            user=request.user,
            payment_gateway='ZarinPal',
            transaction_number='TRX-' + str(basket_id)
        )

        data = {
            'merchant_id': ZARINPAL_MERCHANT_ID,
            'amount': basket.price,
            'description': f'پرداخت برای سبد خرید {basket_id}',
            'callback_url': f'{settings.CALLBACK_URL}/payment/callback/',
            'metadata': {
                'email': request.user.email,
                'mobile': request.user.profile.phone_number
            }
        }

        response = requests.post(ZARINPAL_REQUEST_URL, json=data)
        result = response.json()

        if result.get('data') and result['data']['code'] == 100:
            authority = result['data']['authority']
            transaction.transaction_number = authority
            transaction.save()

            return Response({
                'url': ZARINPAL_START_PAY_URL.format(authority=authority)
            }, status=status.HTTP_200_OK)

        return Response({"error": "Error in payment initiation"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ZarinpalCallback(APIView):
    def get(self, request):
        authority = request.GET.get('Authority')
        status = request.GET.get('Status')

        try:
            transaction = Transaction.objects.get(transaction_number=authority)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        if status == 'OK':
            data = {
                'merchant_id': ZARINPAL_MERCHANT_ID,
                'amount': transaction.price,
                'authority': authority
            }

            response = requests.post(ZARINPAL_VERIFY_URL, json=data)
            result = response.json()

            if result.get('data') and result['data']['code'] == 100:
                transaction.state = Transaction.State.SUCCESSFUL
                transaction.save()

                basket = SaleBasket.objects.get(transaction=transaction)
                basket.state = SaleBasket.State.PAY_SUCCESS
                basket.save()

                return Response({"message": "Payment successful"}, status=status.HTTP_200_OK)

            transaction.state = Transaction.State.FAILED
            transaction.save()
            return Response({"error": "Payment failed during verification"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.state = Transaction.State.FAILED
        transaction.save()

        return Response({"error": "Payment not successful"}, status=status.HTTP_400_BAD_REQUEST)

class CheckTransactionStatus(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "transaction_id": transaction.id,
            "status": transaction.state,
            "payment_gateway": transaction.payment_gateway,
            "price": transaction.price
        }, status=status.HTTP_200_OK)

