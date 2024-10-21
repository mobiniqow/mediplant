from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import SaleBasket


class CreateBasket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        session_key = request.session.session_key
        shop = request.data.get('shop_id')

        basket = SaleBasket.objects.create(
            user=user,
            session_key=session_key,
            shop_id=shop,
            price=0,
            address=request.data.get('address', ''),
            discount=request.data.get('discount', 0)
        )

        return Response({
            "message": "Basket created successfully",
            "basket_id": basket.id
        }, status=status.HTTP_201_CREATED)


class AddProductToBasket(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, basket_id):
        basket = SaleBasket.objects.get(id=basket_id, user=request.user)
        product_id = request.data.get('product_id')
        unit = request.data.get('unit', 1)

        product = ShopProduct.objects.get(id=product_id)
        SaleBasketProduct.objects.create(basket=basket, product=product, unit=unit)

        basket.price += product.price * unit
        basket.save()

        return Response({"message": "Product added to basket"}, status=status.HTTP_200_OK)


class UpdateProductUnit(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, basket_id, product_id):
        basket_product = SaleBasketProduct.objects.get(basket_id=basket_id, product_id=product_id)
        new_unit = request.data.get('unit')

        if new_unit <= 0:
            return Response({"error": "Unit must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        # Update total price
        basket = basket_product.basket
        basket.price -= basket_product.product.price * basket_product.unit
        basket_product.unit = new_unit
        basket_product.save()
        basket.price += basket_product.product.price * new_unit
        basket.save()

        return Response({"message": "Product unit updated"}, status=status.HTTP_200_OK)


class RemoveProductFromBasket(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, basket_id, product_id):
        basket_product = SaleBasketProduct.objects.get(basket_id=basket_id, product_id=product_id)

        # Update total price
        basket = basket_product.basket
        basket.price -= basket_product.product.price * basket_product.unit
        basket_product.delete()
        basket.save()

        return Response({"message": "Product removed from basket"}, status=status.HTTP_200_OK)


class Checkout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, basket_id):
        basket = SaleBasket.objects.get(id=basket_id, user=request.user)

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

