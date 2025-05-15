from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from shop.models import ShopProduct, Shop
from transaction.models import Transaction
from transaction.serializers import TransactionSerializer
from .models import SaleBasket, SaleBasketProduct
from django.shortcuts import get_object_or_404

from .serializers import BaseProductSerializer, BasketSerializer
from rest_framework.exceptions import ValidationError


class CreateDeleteBasket(APIView):
    def post(self, request, shopid):
        user = request.user
        # todo injaro ok konam
        basket, created = SaleBasket.objects.get_or_create(
            user=user,
        )
        basket.address = request.data.get('address', '')
        basket.discount = request.data.get('discount', 0)
        product = SaleBasketProduct.objects.filter(basket=basket)
        items = BaseProductSerializer(product, many=True).data
        return Response({
            "basket_id": basket.id,
            "items": items,
            "price": basket.price,
        }, status=status.HTTP_201_CREATED)

    def delete(self, request, shopid):
        print(f"shop_id received: {shopid}")
        print(f"shop_id {shopid}")
        session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
        # shop = get_object_or_404(Shop, pk=shopid)
        user = request.user

        filters = {
            "pk": shopid,
            "state__lte": SaleBasket.State.IN_PAY  # اصلاح این قسمت
        }
        if user.is_authenticated:
            filters["user"] = user
        else:
            filters["session_key"]: session_key
        deleted_count, _ = SaleBasket.objects.filter(**filters).delete()
        print(f"Deleted {deleted_count} baskets")

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, shopid):
        print(f"request.user.id{request.user.id}")
        basket, _ = SaleBasket.objects.get_or_create(user=request.user, state__lte=SaleBasket.State.IN_PAY)
        # if not basket.exists():
        #     return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        print(111)
        # basket = basket.first()
        product = SaleBasketProduct.objects.filter(basket=basket)
        items = BaseProductSerializer(product, many=True).data
        print(f"price received: {basket.price}")
        return Response({
            "basket_id": basket.id,
            "items": items,
            "price": basket.price,
        }, status=status.HTTP_200_OK)

    def patch(self, request, shopid):
        print(f'shopid {shopid}')
        user = request.user
        product_id = shopid
        unit = request.data.get('unit')

        if not product_id or unit is None:
            return Response({"detail": "product_id و unit الزامی هستند."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            unit = int(unit)
            if unit < 1:
                raise ValidationError("تعداد باید حداقل ۱ باشد.")
        except (ValueError, TypeError):
            return Response({"detail": "تعداد نامعتبر است."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            basket = SaleBasket.objects.get(user=user, state__lte=SaleBasket.State.IN_PAY)
        except SaleBasket.DoesNotExist:
            return Response({"detail": "سبد خرید یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        try:
            basket_product = SaleBasketProduct.objects.get(basket=basket, id=product_id)
        except SaleBasketProduct.DoesNotExist:
            return Response({"detail": "محصول در سبد یافت نشد."}, status=status.HTTP_404_NOT_FOUND)

        # به‌روزرسانی تعداد
        basket_product.unit = unit
        basket_product.save()

        return Response({"detail": "تعداد با موفقیت به‌روزرسانی شد."}, status=status.HTTP_200_OK)

class DeleteProductFromBasket(APIView):
    def delete(self, request, shop_id, product_id):
        if request.user.is_authenticated:
            basket = SaleBasket.objects.filter(shop_id=shop_id, user=request.user,
                                               state__lte=SaleBasket.State.IN_PAY).first()
        else:
            session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(shop_id=shop_id, session_key=session_key,
                                               state__lte=SaleBasket.State.IN_PAY).first()
        if not basket:
            return Response({"error": "Basket not found"}, status=status.HTTP_404_NOT_FOUND)

        # بررسی وجود محصول در سبد خرید
        print(SaleBasketProduct.objects.filter(basket=basket, product_id=product_id))
        basket_product = SaleBasketProduct.objects.filter(basket=basket, id=product_id).first()
        if not basket_product:
            return Response({"error": "Product not found in the basket"}, status=status.HTTP_404_NOT_FOUND)

        # # بروزرسانی قیمت کل
        basket.price -= basket_product.product.price * basket_product.unit
        basket_product.delete()
        basket.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, shop_id, product_id):
        if request.user.is_authenticated:
            basket = SaleBasket.objects.filter(shop_id=shop_id, user=request.user)
        else:
            session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(shop_id=shop_id, session_key=session_key)
        if not basket.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        basket = basket.first()
        basket_product = SaleBasketProduct.objects.filter(basket=basket, id=product_id)
        if not basket_product.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        basket_product = basket_product.first()
        new_unit = int(request.data['unit'])
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


class ProductToBasket(APIView):
    def post(self, request, basket_id, product_id):
        basket = SaleBasket.objects.filter(id=basket_id, user=request.user)
        if basket.exists():
            basket = basket[0]
            if basket.user is None:
                basket.user = request.user
                basket.save()
        print(3)
        basket = get_object_or_404(SaleBasket, id=basket_id, user=request.user)
        print(4)
        # else:
        #     session_key = request.session.session_key or request.META.get('REMOTE_ADDR')
        #     basket = SaleBasket.objects.filter(id=basket_id, session_key=session_key)
        #     if not basket.exists():
        #         return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        #     else:
        #         basket = basket[0]

        shop_product = ShopProduct.objects.filter(id=product_id)
        if not shop_product.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        if shop_product.first().capacity < 1:
            return Response({"message": "not capacity found"}, status=status.HTTP_400_BAD_REQUEST)
        product = ShopProduct.objects.get(id=product_id)
        item = SaleBasketProduct.objects.filter(basket=basket, product=product)
        unit = request.data.get('unit', 1)
        if int(unit) > product.capacity:
            if item.exists():
                item = item.first()
                if item.unit > product.capacity:
                    tafazol = item.unit - int(product.capacity)
                    basket.price -= int(product.price) * tafazol
                    item.unit = int(product.capacity)
                    item.save()
            return Response({"error": "Unit capacity exceeds"}, status=status.HTTP_400_BAD_REQUEST)
        if item.exists():
            item = item.first()
            basket.price -= int(product.price) * int(item.unit)
            if unit == "0" or unit == 0:
                SaleBasketProduct.objects.filter(basket=basket, product=product).delete()
            else:
                basket.price += int(product.price) * int(unit)
                item.unit = unit
                item.save()
            basket.save()
        else:
            if unit != 0:
                basket.price += product.price * int(unit)
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
        basket = SaleBasket.objects.filter(id=basket_id, user=request.user).first()
        if not basket:
            return Response({"error": "Basket not found"}, status=status.HTTP_404_NOT_FOUND)
        basket_product = SaleBasketProduct.objects.filter(basket=basket, product_id=product_id).first()
        if not basket_product:
            return Response({"error": "Product not found in the basket"}, status=status.HTTP_404_NOT_FOUND)

        print(12)
        basket.price -= basket_product.product.price * basket_product.unit
        basket_product.delete()
        basket.save()

        return Response({"message": "Product removed from basket"}, status=status.HTTP_200_OK)


class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, basket_id):
        session_key = request.session.session_key or request.META.get('REMOTE_ADDR')

        basket = get_object_or_404(SaleBasket, id=basket_id, user=request.user)
        # basket = get_object_or_404(SaleBasket,id=basket_id,session_key=session_key )

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
            "transaction_id": TransactionSerializer(transaction).data
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


class MyBasket(APIView):
    def get(self, request):
        basket = SaleBasket.objects.filter(user=request.user, state__lte=SaleBasket.State.PAY_FAILED)
        items = SaleBasketProduct.objects.filter(basket=basket.last())
        serializers = BaseProductSerializer(items,many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def delete(self, request, basket_id):
        product = SaleBasketProduct.objects.filter( id=basket_id)
        if not product.exists():
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CancelBasket(APIView):
    def delete(self, request, basket_id):
        transaction = get_object_or_404(Transaction, pk=basket_id, user=request.user)
        basket: SaleBasket = get_object_or_404(SaleBasket, pk=transaction.cart.id, user=request.user)
        basket.state = SaleBasket.State.CANCELLED
        transaction.status = 'cancel'
        transaction.save()
        basket.save()
        return Response()
