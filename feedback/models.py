from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from account.models import User


class FeedbackCart(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0, "در انتظار"
        SUCCESS = 1, "موفق"
        TimeOut = 2, "منقضی‌شده"

    state = models.IntegerField(choices=State.choices, default=State.SUSPEND, verbose_name="وضعیت")
    cart = models.ForeignKey(
        'sale.SaleBasket',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="سبد خرید"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="نامک")
    is_feedback_sent = models.BooleanField(default=False, verbose_name="ارسال‌شده؟")

    class Meta:
        verbose_name = "سبد نظرسنجی"
        verbose_name_plural = "سبدهای نظرسنجی"

    def __str__(self):
        return f"نظرسنجی #{self.id} - {self.get_state_display()}"


class FeedbackObject(models.Model):
    feedback = models.ForeignKey(
        FeedbackCart,
        on_delete=models.CASCADE,
        verbose_name="نظرسنجی"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    product = models.ForeignKey(
        'shop.ShopProduct',
        on_delete=models.CASCADE,
        verbose_name="محصول فروشگاه",
        related_name='feedback_product'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="امتیاز"
    )
    comment = models.TextField(verbose_name="نظر", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    is_approved = models.BooleanField(default=False, verbose_name="تایید شده؟")

    class Meta:
        verbose_name = "نظر کاربر"
        verbose_name_plural = "نظرات کاربران"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.product}"
