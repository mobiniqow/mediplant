from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
import requests
import json
from .models import DoctorTransaction


@api_view(['POST'])
def start_doctor_payment(request):
    user = request.user
    amount = request.data.get('amount')

    if not amount or float(amount) <= 0:
        return JsonResponse({"error": "مبلغ پرداخت نامعتبر است."}, status=400)

    transaction = DoctorTransaction.objects.create(
        user=user,
        amount=amount,
        transaction_type=DoctorTransaction.TransactionState.REQUESTED,
    )

    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    data = {
        'merchant_id': settings.MERCHANT_ID,
        'amount': str(amount),
        'callback_url': settings.CALLBACK_URL,
        'description': f"پرداخت برای پزشک {user.user_name}"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['code'] == 100:
            print(response_data['data'])
            transaction.ref_id = response_data['data']['authority']
            transaction.save()
            return JsonResponse({"payment_url": f"https://payment.zarinpal.com/pg/StartPay/{response_data['data']['authority']}"})
        else:
            return JsonResponse({"error": response_data['data']['message']}, status=400)
    else:
        return JsonResponse({"error": "خطا در ارتباط با زرین‌پال"}, status=500)



@api_view(['POST'])
def generate_doctor_payment_token(request):
    doctor_transaction_id = request.data.get('doctor_transaction_id')
    doctor_transaction = get_object_or_404(DoctorTransaction, id=doctor_transaction_id)
    amount = doctor_transaction.amount
    if amount <= 0:
        return Response({"error": "مبلغ پرداخت نامعتبر است."}, status=400)
    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    data = {
        'merchant_id': settings.MERCHANT_ID,
        'amount': str(int(amount)),
        'callback_url': settings.CALLBACK_URL,
        'description': f"پرداخت برای تراکنش پزشک {doctor_transaction_id}",
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['code'] == 100:
            authority = response_data['data']['authority']
            doctor_transaction.authority = authority
            doctor_transaction.save()
            return JsonResponse({"payment_url": f"https://payment.zarinpal.com/pg/StartPay/{authority}"})
        else:
            return Response({"error": response_data['data']['message']}, status=400)
    else:
        return Response({"error": "خطا در ارتباط با زرین‌پال"}, status=500)
