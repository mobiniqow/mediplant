from django.core.management.base import BaseCommand

from feedback.views import send_feedback_reminder


class Command(BaseCommand):
    help = "ارسال لینک ثبت فیدبک برای خریدهای ۵ روز پیش"

    def handle(self, *args, **kwargs):
        send_feedback_reminder()
        self.stdout.write(self.style.SUCCESS("لینک فیدبک ارسال شد."))
