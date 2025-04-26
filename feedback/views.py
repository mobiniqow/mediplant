from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from sale.models import SaleBasketProduct
from shop.models import ShopProduct
from .models import FeedbackCart, FeedbackObject
from .serializers import FeedbackObjectSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_feedback_products(request, slug):
    """ لیست محصولات خریداری‌شده که باید نظر داده شوند """
    feedback_cart = get_object_or_404(FeedbackCart, slug=slug)

    if feedback_cart.state == FeedbackCart.State.SUCCESS:
        return Response({"error": "شما قبلاً نظرات خود را ثبت کرده‌اید."}, status=400)

    purchased_products = SaleBasketProduct.objects.filter(basket=feedback_cart.cart)
    feedback_objects = FeedbackObject.objects.filter(feedback=feedback_cart, user=request.user)

    # بررسی محصولاتی که هنوز نظری برای آن‌ها ثبت نشده
    pending_products = []
    for item in purchased_products:
        if not feedback_objects.filter(product=item.product).exists():
            pending_products.append(item.product)

    return Response({
        "feedback_cart": feedback_cart.slug,
        "pending_products": [p.id for p in pending_products],
        "feedbacks": FeedbackObjectSerializer(feedback_objects, many=True).data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_feedback(request, slug, product_id):
    feedback_cart = get_object_or_404(FeedbackCart, slug=slug)
    if feedback_cart.state == FeedbackCart.State.SUCCESS:
        return Response({"error": "شما دیگر نمی‌توانید نظرات را تغییر دهید."}, status=400)
    product = get_object_or_404(ShopProduct, id=product_id)
    rating = request.data.get("rating")
    comment = request.data.get("comment", "").strip()
    if rating is None:
        return Response({"error": "امتیاز (rating) الزامی است."}, status=400)
    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return Response({"error": "امتیاز باید بین ۱ تا ۵ باشد."}, status=400)
    except ValueError:
        return Response({"error": "امتیاز باید عدد صحیح باشد."}, status=400)

    feedback_obj, created = FeedbackObject.objects.get_or_create(
        feedback=feedback_cart, user=request.user, product=product,
        defaults={"rating": rating, "comment": comment}
    )

    if not created:
        feedback_obj.rating = rating
        feedback_obj.comment = comment
        feedback_obj.save()

    serializer = FeedbackObjectSerializer(feedback_obj)

    return Response({
        "message": "نظر شما ثبت شد." if created else "نظر شما به‌روزرسانی شد.",
        "data": serializer.data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finalize_feedback(request, slug):
    """ نهایی‌سازی ثبت نظرات """
    feedback_cart = get_object_or_404(FeedbackCart, slug=slug)

    purchased_products = SaleBasketProduct.objects.filter(basket=feedback_cart.cart)
    feedback_objects = FeedbackObject.objects.filter(feedback=feedback_cart)

    # بررسی اینکه آیا برای همه محصولات نظر ثبت شده است
    if feedback_objects.count() < purchased_products.count():
        return Response({"error": "لطفاً برای تمام محصولات نظر خود را ثبت کنید."}, status=400)

    feedback_cart.state = FeedbackCart.State.SUCCESS
    feedback_cart.save()

    return Response({"message": "نظرات شما نهایی شد و برای تأیید ارسال گردید."})

@api_view(['GET'])
def get_approved_feedbacks(request, shop_id, product_id):
    shop_products = ShopProduct.objects.filter(shop_id=shop_id, product_id=product_id)
    print(shop_products)
    feedbacks = FeedbackObject.objects.filter(product__in=shop_products, is_approved=True)

    serializer = FeedbackObjectSerializer(feedbacks, many=True)
    return Response(serializer.data)

