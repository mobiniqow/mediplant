from django.core.validators import MinValueValidator
from django.db import models
from account.models import User
from shop.models import Shop, ShopProduct
import jdatetime


class SaleBasket(models.Model):
    class State(models.IntegerChoices):
        SUSPEND = 0
        IN_PAY = 1
        PAY_FAILED = 2
        PAY_SUCCESS = 3
        IN_SHOP_COMPILATION = 4
        SENDING = 5
        SEND_BACK = 6
        IN_POST_OFFICE = 7
        DONE_AND_FINISH = 8
        CANCELLED = 9
        SHOP_CANCEL = 10

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name='کاربر')
    session_key = models.CharField(max_length=200, null=True, verbose_name='کلید جلسه')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='قیمت', )
    address = models.TextField(verbose_name='آدرس')
    state = models.IntegerField(choices=State.choices, default=0, verbose_name='وضعیت')
    discount = models.IntegerField(validators=[MinValueValidator(0)], verbose_name='تخفیف')
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, verbose_name='فروشگاه')
    transaction = models.ForeignKey('transaction.Transaction', on_delete=models.SET_NULL, null=True,
                                    verbose_name='تراکنش', blank=True)
    delivery_date = models.DateField(null=True, blank=True, verbose_name='زمان تحویل')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد‌های خرید'

    def get_delivery_date(self):
        """تبدیل تاریخ میلادی به تاریخ شمسی"""
        return jdatetime.datetime.fromgregorian(datetime=self.delivery_date).strftime('%Y/%m/%d')

    def __str__(self):
        state_display = self.get_state_display()
        return f"سبد خرید برای {self.user} - وضعیت: {state_display} - قیمت: {self.price} تومان"


class SaleBasketProduct(models.Model):
    basket = models.ForeignKey('SaleBasket', on_delete=models.SET_NULL, null=True, verbose_name='سبد خرید')
    product = models.ForeignKey(ShopProduct, on_delete=models.SET_NULL, null=True, verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    unit = models.IntegerField(default=0, validators=[MinValueValidator(0)], verbose_name='تعداد')

    class Meta:
        verbose_name = 'محصول سبد خرید'
        verbose_name_plural = 'محصولات سبد خرید'

    def __str__(self):
        return f"{self.product} - {self.unit} واحد در {self.basket}"
