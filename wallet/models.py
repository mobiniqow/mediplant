from django.db import models
import uuid


class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    user = models.OneToOneField('account.User', on_delete=models.CASCADE, verbose_name='کاربر')
    amount = models.IntegerField(verbose_name='موجودی', default=0)
    description = models.TextField(verbose_name='توضیحات')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='تاریخ بروزرسانی')

    def __str__(self):
        return f"کیف پول {self.user} - موجودی: {self.amount} تومان"

    def get_amount(self):
        return self.amount

    def pay(self, amount):
        if self.amount >= amount:
            self.amount -= amount
            self.save()
            return True, 0
        else:

            return False, amount - self.amount

    @staticmethod
    def pay_from_user(user, amount):
        wallet = Wallet.objects.get_or_create(user=user)[0]
        return wallet.pay(amount)
