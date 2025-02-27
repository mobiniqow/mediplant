from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from abstract_view.base_template_view import BaseTemplateView
from banner.models import Banner
from encyclopedia.models import ArticleEncyclopedia
from product.models import Category, Product, ProductImage
from sale.models import SaleBasket, SaleBasketProduct
from shop.models import ShopProduct, Shop, ShopImage
import math

from transaction.models import Transaction, Payment


class IndexView(BaseTemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        top_banners = Banner.objects.filter(state=Banner.State.ACTIVE, type=Banner.Type.INDEX_TOP_SLIDER).order_by('?')[
                      :6]
        two_banners = Banner.objects.filter(state=Banner.State.ACTIVE, type=Banner.Type.INDEX_TWO_SLIDER).order_by('?')[
                      :2]
        middle_banner = Banner.objects.filter(state=Banner.State.ACTIVE, type=Banner.Type.INDEX_MIDDLE_SLIDER).order_by(
            '?').first()
        bottom_banner = Banner.objects.filter(state=Banner.State.ACTIVE, type=Banner.Type.INDEX_BOTTOM_SLIDER).order_by(
            '?')[:2]
        # کالا ها با عکس
        for i in ShopProduct.objects.all():
            i.inventory_state = ShopProduct.Inventory.AVAILABLE
            i.save()

        shop_products = ShopProduct.objects.filter(inventory_state=ShopProduct.Inventory.AVAILABLE)
        product_ids = [shop_product.product_id for shop_product in shop_products]
        products = Product.objects.select_related('class_id', 'category', 'unit').prefetch_related('images').filter(
            id__in=product_ids)[:10]
        # برای اینکه عکس ها از حالت این لاین در بیان
        for i in products:
            i.image_list = i.images.all()
        new_product = Product.objects.select_related('class_id', 'category', 'unit').prefetch_related(
            'images').order_by('id').filter(is_active=True)[:12]
        for i in new_product:
            i.image_list = i.images.all()
        # moamelat roz
        day_product = Product.objects.select_related('class_id', 'category', 'unit').prefetch_related(
            'images').order_by('id').filter(is_active=True)[:12]
        for i in day_product:
            i.image_list = i.images.all()
        # top 10 shops
        best_shops = Shop.objects.all()[:10]
        for i in best_shops:
            i.images_list = []
            i.product_number = len(ShopProduct.objects.filter(shop=i))
            for j in ShopProduct.objects.filter(shop=i)[:4]:
                i.images_list.append(
                    {"image": ProductImage.objects.filter(product=j.product).first(), "product_id": j.id})
        articles = ArticleEncyclopedia.objects.all()[:7]
        context['title'] = 'صفحه اصلی'
        context['top_banners'] = top_banners
        context['two_banners'] = two_banners
        context['middle_banner'] = middle_banner
        context['bottom_banner'] = bottom_banner
        context['articles'] = articles
        context['new_product'] = new_product
        context['day_product'] = day_product
        context['best_shops'] = best_shops
        context['products'] = products
        # todo after works in item ha query dorost mikhorands
        context['best_seller'] = products
        context['new_product'] = products
        context['most_views'] = products
        # todo after works in item ha query dorost mikhorands
        context['bot_3_new_product'] = products[:3]
        context['bot_3_most_sell'] = products[:3]
        context['bot_3_best_rank'] = products[:3]
        context['bot_3_most_popular'] = products[:3]
        return context


class CategoryView(BaseTemplateView):
    template_name = "shop/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(parent=None)

        banners = Banner.objects.filter(state=Banner.State.ACTIVE, type=Banner.Type.SEARCH_TOP_TWO_BANNER).order_by(
            '?')[:2]

        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        context['categories'] = categories

        return context


class ShopView(BaseTemplateView):
    template_name = "shop/shop-list-banner-left-sidebar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}

        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        categories = Category.objects.filter(parent=None)

        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        banners = Banner.objects.filter(state=Banner.State.ACTIVE).order_by('?')[:6]
        shops = Shop.objects.filter(state=Shop.ShopStatus.ACTIVE)

        context['shops'] = shops
        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        context['categories'] = categories
        context['categories_map'] = category_and_sub_category
        return context


class ShopDetailsView(BaseTemplateView):
    template_name = "shop/shop-details.html"

    def get_context_data(self, **kwargs):
        page_size = 15
        context = super().get_context_data(**kwargs)
        shop_id = kwargs['id']
        shop = get_object_or_404(Shop, pk=shop_id)
        banners = ShopImage.objects.filter(shop=shop)
        shop.banners = ShopImage.objects.filter(shop=shop)
        product = ShopProduct.objects.filter(shop=shop)
        page_number = math.ceil(product.count() / page_size)

        for i in product:
            i.image = ProductImage.objects.filter(product=i.product).first()
            i.price = '{:,.0f}'.format(i.price)

        context['shop'] = shop
        context['banners'] = banners
        context['product'] = [product[i:i + page_size] for i in range(0, len(product), page_size)]
        context['page_number'] = [i for i in range(1, page_number + 1)]

        if self.request.user.is_anonymous:
            print('asal')
            session_key = self.request.session.session_key or self.request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(session_key=session_key, state__lte=SaleBasket.State.IN_PAY, shop=shop)
            products = SaleBasketProduct.objects.filter(basket__in=basket)
        else:
            basket = SaleBasket.objects.filter(user=self.request.user, state__lte=SaleBasket.State.IN_PAY,
                                               shop=shop).first()
            products = SaleBasketProduct.objects.filter(basket=basket)
            print(f'sdsda {products}')
            print(
                f'sdsda {SaleBasket.objects.filter(user=self.request.user, state__lte=SaleBasket.State.IN_PAY, shop=shop).count()}')
        context['cart_product'] = products
        context['shop_notification'] = len(products)
        return context


class SearchProduct(BaseTemplateView):
    template_name = 'shop/search-product-in-shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs['product_id']
        shops_product = ShopProduct.objects.filter(product_id=product_id).order_by('price')
        products = Product.objects.select_related('class_id', 'category', 'unit').prefetch_related('images')[:10]
        for i in shops_product:
            i.image = ProductImage.objects.filter(product=i.product).first()
        for i in products:
            i.image_list = i.images.all()
        context['products'] = products
        context['product_shops'] = shops_product
        return context


class CheckoutView(BaseTemplateView):
    template_name = 'shop/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ShopCartView(BaseTemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        page_size = 15
        context = super().get_context_data(**kwargs)
        shop_id = kwargs['id']
        shop = get_object_or_404(Shop, pk=shop_id)
        basket = get_object_or_404(SaleBasket, shop=shop, state__in=[
            SaleBasket.State.SUSPEND,
            SaleBasket.State.IN_PAY,
            SaleBasket.State.PAY_FAILED
        ])
        product = SaleBasketProduct.objects.filter(basket=basket)
        for i in product:
            i.image = ProductImage.objects.filter(product=i.product.product).first()
            i.price = '{:,.0f}'.format(i.product.price)
            i.price_all = '{:,.0f}'.format(i.product.price * i.unit)
        print(self.request.user.postal_code)
        context['user'] = self.request.user
        context['shop'] = shop
        context['product'] = product

        return context


class AfterBankGateWay(BaseTemplateView):
    template_name = "shop/track-order.html"

    def get_context_data(self, **kwargs):
        page_size = 15
        context = super().get_context_data(**kwargs)
        shop_id = kwargs['id']

        transaction = Transaction.objects.get(id=shop_id)
        shop = get_object_or_404(Shop, pk=transaction.cart.shop.id)

        basket = get_object_or_404(SaleBasket, shop=shop, state__in=[
            SaleBasket.State.SUSPEND,
            SaleBasket.State.IN_PAY,
            SaleBasket.State.PAY_FAILED
        ])
        product = SaleBasketProduct.objects.filter(basket=basket)
        for i in product:
            i.image = ProductImage.objects.filter(product=i.product.product).first()
            i.price = '{:,.0f}'.format(i.product.price)
            i.price_all = '{:,.0f}'.format(i.product.price * i.unit)

        context['user'] = self.request.user
        context['shop'] = shop
        context['product'] = product

        context['date'] = basket.get_delivery_date()
        context['step'] = 4
        context['transaction'] = transaction

        return context


class OrderListView(TemplateView):
    template_name = "shop/order_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}

        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        categories = Category.objects.filter(parent=None)

        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        banners = Banner.objects.filter(state=Banner.State.ACTIVE).order_by('?')[:6]
        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        context['categories'] = categories
        context['categories_map'] = category_and_sub_category

        return context


class CallbackView(BaseTemplateView):
    template_name = "shop/call-back.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        authority = self.request.GET.get('Authority', None)
        status = self.request.GET.get('Status', None)

        # گرفتن تراکنش بر اساس Authority
        transaction = Transaction.objects.filter(authority=authority).first()
        shop_id = Payment.objects.filter(transaction=transaction).first().cart.shop.id
        # جزئیات تراکنش
        transaction_details = transaction.get_transaction_details()

        # پیام مناسب بسته به وضعیت پرداخت
        if status == "OK":
            payment_status_message = "پرداخت با موفقیت انجام شد"
        else:
            payment_status_message = "پرداخت ناموفق"

        context['payment_status_message'] = payment_status_message
        context['authority'] = authority
        context['status'] = status
        context['shop_id'] = shop_id
        context['transaction'] = transaction
        context['transaction_details'] = transaction_details
        return context


class ShopTransactions(BaseTemplateView):
    template_name = 'shop/transactions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ShopCartDetailsOrderView(BaseTemplateView):
    template_name = "shop/cart_details_order.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transaction_id = kwargs['id']
        transaction = get_object_or_404(Transaction, pk=transaction_id)
        cart = transaction.cart
        products = SaleBasketProduct.objects.filter(basket=cart)
        transaction.amount = f'{int(transaction.amount):,}'
        for i in products:
            i.image = ProductImage.objects.filter(product=i.product.product).first()
            i.price = '{:,.0f}'.format(i.product.price)
            i.price_all = '{:,.0f}'.format(i.product.price * i.unit)
        context['user'] = self.request.user
        context['products'] = products
        context['transaction'] = transaction
        print(transaction.id)
        print(cart.state)
        context['cancelable'] = (transaction.status == 'pending' or cart.state == SaleBasket.State.IN_PAY
                                 or cart.state == SaleBasket.State.PAY_FAILED)
        context['buyable'] = (transaction.status == 'pending' or cart.state == SaleBasket.State.PAY_FAILED)

        return context
