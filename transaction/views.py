from sale.models import SaleBasket
from .models import Transaction, Payment
import requests
import json
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect
@api_view(['POST', ])
def start_payment(request, shop_id):
    user = request.user
    cart = get_object_or_404(SaleBasket, user=user, pk=shop_id)
    if not cart:
        return JsonResponse({"error": "سبد خرید یافت نشد"})
    amount = cart.price
    address = request.data.get('address')
    lat = request.data.get('lat')
    lng = request.data.get('lng')
    code_posti = request.data.get('code_posti')
    print(address)
    print(lat)
    print(lng)
    print(code_posti)
    transaction = Transaction.objects.create(
        user=user,
        cart=cart,
        amount=amount,
        transaction_type='deposit',
        status='pending',
        message=f"پرداخت برای سبد خرید {user.user_name}",
        address=address,
        lat=lat,
        lng=lng,
        code_posti=code_posti
    )

    # ایجاد پرداخت جدید
    payment = Payment.objects.create(
        user=user,
        cart=cart,
        transaction=transaction
    )

    # شروع پرداخت از طریق زرین‌پال
    try:
        payment_url = payment.initiate_payment()
        return JsonResponse({"payment_url": payment_url})
    except Exception as e:
        return JsonResponse({"error": str(e)})


@api_view(['GET'])
def verify_payment(request):
    # دریافت پارامترهای Authority و Status از URL
    status = request.GET.get("Status")
    authority = request.GET.get("Authority")

    # دریافت اطلاعات پرداخت
    try:
        payment = Payment.objects.get(transaction__authority=authority)
    except Payment.DoesNotExist:
        return JsonResponse({"error": "پرداخت یافت نشد"})

    if status == "OK":
        # ارسال درخواست تایید پرداخت از زرین‌پال
        url = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
        data = {
            'merchant_id': settings.MERCHANT_ID,
            'amount': payment.cart.price,
            'authority': authority
        }
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=json.dumps(data), headers=headers)
        print(response.text)

        if response.status_code == 200:
            response_data = response.json()
            if response_data['data']['code'] in [100, 101]:
                # تایید پرداخت موفق
                transaction = Transaction.objects.filter(authority=authority).first()
                if transaction:
                    transaction.status = 'success'
                    transaction.save()
                    print(response_data['data']['card_pan'])

                    # بروزرسانی وضعیت پرداخت
                    payment.status = 'completed'
                    transaction.card = response_data['data']['card_pan']
                    transaction.card_hash = response_data['data']['card_hash']
                    transaction.ref_id = response_data['data']['ref_id']

                    sb = SaleBasket.objects.filter(id=payment.cart.id).first()
                    sb.state = SaleBasket.State.PAY_SUCCESS
                    sb.save()

                    transaction.save()
                    payment.save()

                    # ریدایرکت به /callback/ با پارامترهای Authority و Status
                    return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=OK")
                else:
                    return JsonResponse({"error": "تراکنش یافت نشد"})
            else:
                # ریدایرکت به /callback/ با پارامترهای Authority و Status و خطا
                return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=FAILED")
        else:
            # ریدایرکت به /callback/ با پارامترهای Authority و Status و خطا در ارتباط
            return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=ERROR")
    else:
        # ریدایرکت به /callback/ در صورتی که Status برابر با OK نباشد
        return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=FAILED")

@api_view(['POST'])
def get_payment_url(request):
    user = request.user
    cart_id = request.data.get('cart_id')

    cart = SaleBasket.objects.filter(user=user, id=cart_id).first()

    if not cart:
        return JsonResponse({"error": "سبد خرید یافت نشد"}, status=404)

    total_amount = sum(item.course.price * item.quantity for item in cart.items.all())

    if total_amount <= 0:
        return JsonResponse({"error": "سبد خرید خالی است یا مبلغ پرداخت صحیح نیست."}, status=400)

    transaction = Transaction.objects.create(
        wallet=user.wallet,
        amount=total_amount,
        transaction_type='deposit',
        status='pending',
        message=f"پرداخت برای سبد خرید {cart_id}"
    )

    url = "https://api.zarinpal.com/pg/v4/payment/request.json"
    data = {
        'merchant_id': settings.MERCHANT_ID,
        'amount': total_amount,
        'callback_url': settings.CALLBACK_URL,
        'description': f"پرداخت برای سبد خرید {cart_id}"
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = response.json()

        if response_data['data']['code'] == 100:
            authority = response_data['data']['authority']
            transaction.authority = authority
            transaction.save()

            payment_url = response_data['data']['url']
            return JsonResponse({"payment_url": payment_url})

        else:
            return JsonResponse({"error": response_data['data']['message']}, status=400)

    else:
        return JsonResponse({"error": "خطا در ارتباط با زرین‌پال"}, status=500)


@api_view(['GET'])
def get_transactions(request):
    user = request.user
    transactions = Transaction.objects.filter(user=user).values(
        'id', 'transaction_type', 'amount', 'status', 'timestamp', 'message', 'authority'
    )

    if not transactions:
        return JsonResponse({"error": "تراکنشی یافت نشد"}, status=404)

    return JsonResponse(list(transactions), safe=False)



class ListTransactions(APIView):
    def get(self,request,**kwargs):
        print(request.user.is_authenticated)
        transactions = Transaction.objects.all().select_related('cart', 'cart__shop')
        transaction_data = []
        for transaction in transactions:
            transaction_info = {
                'date': transaction.get_shamsi_date(),
                'shop': transaction.cart.shop.name if transaction.cart and transaction.cart.shop else 'Unknown Shop',
                'shop_id': transaction.cart.shop.id if transaction.cart and transaction.cart.shop else 'Unknown Shop',
                'transaction_id': transaction.id,
                'amount': transaction.amount,
                'items_count': transaction.cart.salebasketproduct_set.count() if transaction.cart else 0,
                'status': transaction.status,
            }

            transaction_data.append(transaction_info)

        return Response(transaction_data)