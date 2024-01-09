from django.views.generic import TemplateView

from banner.models import Banner
from product.models import Category, Product, ProductImage
from shop.models import ShopProduct, Shop


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = Banner.objects.filter(state=Banner.State.ACTIVE).order_by('?')[:6]
        categories = Category.objects.filter(parent=None)
        # کالا ها با عکس
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
        best_shops = Shop.objects.all()
        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        context['new_product'] = new_product
        context['day_product'] = day_product

        context['products'] = products
        context['categories'] = categories
        return context
