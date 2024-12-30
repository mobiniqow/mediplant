from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from shop.models import ShopProduct, Shop
from transaction.models import Transaction
from .models import SaleBasket, SaleBasketProduct
from django.shortcuts import get_object_or_404

from .serializers import BaseProductSerializer


class CreateBasket(APIView):
    def post(self, request, shop_id):
        session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
        shop = get_object_or_404(Shop, pk=shop_id)
        user = request.user
        if user.is_authenticated:
            basket, created = SaleBasket.objects.get_or_create(
                shop=shop,
                user=user,
                session_key=session_key,
                defaults={
                    'price': 0,
                    'address': request.data.get('address', ''),
                    'discount': request.data.get('discount', 0)
                }
            )
        else:
            basket, created = SaleBasket.objects.get_or_create(
                shop=shop,
                session_key=session_key,
                defaults={
                    'price': 0,
                    'address': request.data.get('address', ''),
                    'discount': request.data.get('discount', 0)
                }
            )
        product = SaleBasketProduct.objects.filter(basket=basket)
        items = BaseProductSerializer(product, many=True).data
        return Response({
            "basket_id": basket.id,
            "items": items,
            "price": basket.price,
        }, status=status.HTTP_201_CREATED)


class ProductToBasket(APIView):
    def post(self, request, basket_id, product_id):
        print(request.user)
        if request.user != None:
            session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(id=basket_id, session_key=session_key)
            if basket.exists():
                basket = basket[0]
                if basket.user is None:
                    basket.user = request.user
                    basket.save()
            basket = get_object_or_404(SaleBasket,id=basket_id, user=request.user)
        else:
            session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(id=basket_id, session_key=session_key)
            if not basket.exists():
                return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
            else:
                basket = basket[0]
        shop_product = ShopProduct.objects.filter(id=product_id, shop=basket.shop)
        if not shop_product.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        if shop_product.first().capacity < 1:
            return Response({"message": "not capacity found"}, status=status.HTTP_400_BAD_REQUEST)
        product = ShopProduct.objects.get(id=product_id)
        item = SaleBasketProduct.objects.filter(basket=basket, product=product)
        unit = request.data.get('unit', 1)
        if item.exists():
            item = item.first()
            basket.price -= int(product.price) * int(item.unit)
            if unit == "0"or unit == 0:
                SaleBasketProduct.objects.filter(basket=basket, product=product).delete()
            else:
                basket.price += int(product.price) * int(unit)
                item.unit = unit
                item.save()
            basket.save()
        else:
            if unit != 0:
                basket.price+=product.price * int(unit)
                basket.save()
                SaleBasketProduct.objects.create(basket=basket, product=product, unit=unit, )
        return Response({"message": "Product added to basket"}, status=status.HTTP_200_OK)

    def put(self, request, basket_id, product_id):
        if request.user.is_authenticated:
            basket = SaleBasket.objects.filter(id=basket_id, user=request.user)
        else:
            session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(id=basket_id, session_key=session_key)
        if not basket.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        basket = basket.first()
        basket_product = SaleBasketProduct.objects.filter(basket=basket, product_id=product_id)
        if not basket_product.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        basket_product = basket_product.first()
        new_unit = int(request.data.get('unit'))
        if new_unit <= 0:
            return Response({"error": "Unit must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)
        product = get_object_or_404(ShopProduct, pk=product_id)
        if new_unit > product.capacity:
            return Response({"error": "Unit capacity exceeds"}, status=status.HTTP_400_BAD_REQUEST)
        basket = basket_product.basket
        basket.price -= basket_product.product.price * basket_product.unit
        basket_product.unit = new_unit
        basket_product.save()
        basket.price += basket_product.product.price * new_unit
        basket.save()
        return Response({"message": "Product unit updated"}, status=status.HTTP_200_OK)

    def delete(self, request, basket_id, product_id):
        if request.user.is_authenticated:
            basket = SaleBasket.objects.filter(id=basket_id, user=request.user).first()
        else:
            session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(id=basket_id, session_key=session_key).first()

        # بررسی وجود سبد خرید
        if not basket:
            return Response({"error": "Basket not found"}, status=status.HTTP_404_NOT_FOUND)

        # بررسی وجود محصول در سبد خرید
        basket_product = SaleBasketProduct.objects.filter(basket=basket, product_id=product_id).first()
        if not basket_product:
            return Response({"error": "Product not found in the basket"}, status=status.HTTP_404_NOT_FOUND)

        # بروزرسانی قیمت کل
        basket.price -= basket_product.product.price * basket_product.unit
        basket_product.delete()
        basket.save()

        return Response({"message": "Product removed from basket"}, status=status.HTTP_200_OK)


class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, basket_id):
        session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
        basket = SaleBasket.objects.filter(id=basket_id, user=request.user)
        if not basket.exists():
            basket = SaleBasket.objects.filter(id=basket_id, session_key=session_key)
            if not basket.exists():
                return Response({"error": "Basket is not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                basket = basket.first()
                basket.user = request.user
                basket.session_key = None
                basket.save()

        if basket.price <= 0:
            return Response({"error": "Basket is empty"}, status=status.HTTP_400_BAD_REQUEST)

        transaction = Transaction.objects.create(
            price=basket.price,
            user=request.user,
            payment_gateway=request.data.get('payment_gateway', 'default_gateway'),
            transaction_number=request.data.get('transaction_number', 'TRX-' + str(basket_id))
        )

        basket.transaction = transaction
        basket.state = SaleBasket.State.IN_PAY
        basket.save()

        return Response({
            "message": "Transaction initiated",
            "transaction_id": transaction.id
        }, status=status.HTTP_201_CREATED)


class UpdateTransactionStatus(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_id):
        transaction = Transaction.objects.get(id=transaction_id, user=request.user)
        new_state = request.data.get('state')

        if new_state not in dict(Transaction.State.choices).keys():
            return Response({"error": "Invalid state"}, status=status.HTTP_400_BAD_REQUEST)

        transaction.state = new_state
        transaction.save()

        # Update basket status if transaction is successful
        if new_state == Transaction.State.SUCCESSFUL:
            basket = SaleBasket.objects.get(transaction=transaction)
            basket.state = SaleBasket.State.PAY_SUCCESS
            basket.save()

        return Response({"message": "Transaction state updated"}, status=status.HTTP_200_OK)
