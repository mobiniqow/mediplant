from doctor_visit.models import DoctorVisit
from feedback.models import FeedbackCart
from sale.models import SaleBasket
from wallet.models import Wallet
from .models import Transaction, Payment, DoctorTransaction
import requests
import json
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework.views import APIView
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.text import slugify
import uuid


@api_view(['POST'])
def start_payment(request, shop_id):
    user = request.user
    cart = get_object_or_404(SaleBasket, user=user, pk=shop_id)
    if not cart:
        return JsonResponse({"error": "سبد خرید یافت نشد"})

    amount = cart.price

    is_ok, dept = Wallet.pay_from_user(user, amount)
    if is_ok:
        return JsonResponse({"message": "پرداخت با موفقیت انجام شد", })
    else:
        amount = dept
    address = request.data.get('address')
    lat = request.data.get('lat')
    lng = request.data.get('lng')
    code_posti = request.data.get('code_posti')
    card = request.data.get('card')
    transaction = Transaction.objects.filter(
        user=user,
        cart=cart,
        transaction_type='deposit',
        card=card
    ).first()
    if transaction:
        # اگر تراکنش وجود داشت، فقط آپدیت شود
        transaction.amount = amount
        transaction.status = 'pending'
        transaction.message = f"پرداخت برای سبد خرید {user.user_name}"
        transaction.address = address
        transaction.lat = lat
        transaction.lng = lng
        transaction.code_posti = code_posti
        transaction.save()
    else:
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
            code_posti=code_posti,
            card=card
        )
    payment, created = Payment.objects.get_or_create(
        user=user,
        cart=cart,
        transaction=transaction
    )
    try:
        payment_url = payment.initiate_payment()
        return JsonResponse({"payment_url": payment_url})
    except Exception as e:
        return JsonResponse({"error": str(e)})


def create_feedback_cart(user, cart):
    unique_slug = slugify(f"{user.id}-{uuid.uuid4().hex[:8]}")
    feedback_cart = FeedbackCart.objects.create(cart=cart, slug=unique_slug)
    return feedback_cart


@api_view(['GET'])
def verify_payment(request):
    status = request.GET.get("Status")
    authority = request.GET.get("Authority")
    transaction = Transaction.objects.filter(authority=authority).first()
    doctor_transaction = DoctorTransaction.objects.filter(ref_id=authority).first()

    if not transaction and not doctor_transaction:
        return JsonResponse({"error": "تراکنش یافت نشد"}, status=404)

    amount = transaction.amount if transaction else doctor_transaction.amount
    url = "https://payment.zarinpal.com/pg/v4/payment/verify.json"
    data = {
        'merchant_id': settings.MERCHANT_ID,
        'amount': amount,
        'authority': authority
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        if response_data['data']['code'] in [100, 101]:
            if transaction:
                transaction.status = 'success'
                transaction.card = response_data['data']['card_pan']
                transaction.card_hash = response_data['data']['card_hash']
                transaction.ref_id = response_data['data']['ref_id']
                transaction.save()
                payment = Payment.objects.get(transaction=transaction)
                payment.status = 'completed'
                wallet = Wallet.objects.get_or_create(user=transaction.user)[0]
                wallet.amount += transaction.amount
                wallet.save()
                payment.save()

            if doctor_transaction:
                doctor_transaction.transaction_type = DoctorTransaction.TransactionState.ACCEPT
                doctor_transaction.card_hash = response_data['data']['card_hash']
                doctor_transaction.save()

            return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=OK")
        else:
            if transaction:
                transaction.status = 'failed'
                transaction.save()
            if doctor_transaction:
                doctor_transaction.transaction_type = DoctorTransaction.TransactionState.FAILED
                doctor_transaction.save()
            return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=FAILED")
    else:
        if transaction:
            transaction.status = 'failed'
            transaction.save()
        if doctor_transaction:
            doctor_transaction.transaction_type = DoctorTransaction.TransactionState.FAILED
            doctor_transaction.save()
        return HttpResponseRedirect(f"/callback/?Authority={authority}&Status=ERROR")


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
    def get(self, request, **kwargs):
        transactions = Transaction.objects.exclude(status='cancel').select_related('cart', 'cart__shop')
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


class PayFromWalletApi(APIView):
    def post(self, request, **kwargs):
        user = request.user
        amount = request.data.get('amount')
        transaction_type = request.data.get('transaction_type')
        cart_id = request.data.get('cart_id')

        if transaction_type == 'BASKET':
            cart = get_object_or_404(SaleBasket, user=user, pk=cart_id)
            amount = cart.price
        if transaction_type == 'DOCTOR':
            cart = get_object_or_404(DoctorVisit, user=user, pk=cart_id)
            amount = cart.price

        is_ok, dept = Wallet.pay_from_user(user, amount)
        if is_ok:
            return JsonResponse({"message": "پرداخت با موفقیت انجام شد", })
        else:
            return JsonResponse({"error": "موجودی کیف پول کافی نیست", "dept": dept}, status=400)
