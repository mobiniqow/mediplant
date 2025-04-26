from django.utils.timezone import now, timedelta
from django.core.mail import send_mail
from django.conf import settings
from feedback.models import FeedbackCart


def send_feedback_reminder():
    """ کرون‌جاب برای ارسال لینک فیدبک به کاربرانی که ۵ روز از خریدشان گذشته است. """

    five_days_ago = now() - timedelta(days=5)

    feedback_carts = FeedbackCart.objects.filter(
        created_at__lte=five_days_ago,
        state=FeedbackCart.State.SUSPEND,
        is_feedback_sent=False  # فقط مواردی که ارسال نشده‌اند را می‌فرستیم
    )

    for feedback_cart in feedback_carts:
        user_email = feedback_cart.cart.user.email
        feedback_link = f"{settings.FRONTEND_URL}/feedback/{feedback_cart.slug}"

        # ارسال ایمیل یا پیامک به کاربر
        send_mail(
            "ثبت نظر برای خرید شما",
            f"سلام، لطفاً نظر خود را برای محصولات خریداری‌شده ثبت کنید: {feedback_link}",
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )

        # تغییر وضعیت به "ارسال شده"
        feedback_cart.is_feedback_sent = True
        feedback_cart.save()
