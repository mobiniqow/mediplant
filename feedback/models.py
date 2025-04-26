from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User


class FeedbackCart(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        SUCCESS = 1
        TimeOut = 2

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND)
    cart = models.ForeignKey('sale.SaleBasket', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="نامک")
    is_feedback_sent = models.BooleanField(default=False)  # این فیلد بررسی می‌کند که آیا لینک ارسال شده است یا نه.


class FeedbackObject(models.Model):
    feedback = models.ForeignKey(FeedbackCart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey('shop.ShopProduct', on_delete=models.CASCADE, verbose_name="محصول فروشگاه",related_name='feedback_product')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name="امتیاز")
    comment = models.TextField(verbose_name="نظر", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده")


