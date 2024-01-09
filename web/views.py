from django.views.generic import TemplateView

from banner.models import Banner
from product.models import Category, Product, ProductImage
from shop.models import ShopProduct


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
        for i in products:
            i.image_list = i.images.all()
        new_product = 0
        best_seller = 0
        high_rank = 0
        most_popular = 0
        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        context['products'] = products
        context['categories'] = categories
        return context
