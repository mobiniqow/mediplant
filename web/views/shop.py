from django.views.generic import TemplateView

from abstract_view.base_template_view import BaseTemplateView
from banner.models import Banner
from encyclopedia.models import ArticleEncyclopedia
from product.models import Category, Product, ProductImage
from shop.models import ShopProduct, Shop


class IndexView(BaseTemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = Banner.objects.filter(state=Banner.State.ACTIVE).order_by('?')[:6]
        categories = Category.objects.filter(parent=None)
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
        context['banner'] = banners
        context['articles'] = articles
        context['new_product'] = new_product
        context['day_product'] = day_product
        context['best_shops'] = best_shops
        context['products'] = products
        context['categories'] = categories
        return context


class CategoryView(BaseTemplateView):
    template_name = "category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(parent=None)

        banners = Banner.objects.filter(state=Banner.State.ACTIVE).order_by('?')[:6]

        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        context['categories'] = categories

        return context


class ShopView(TemplateView):
    template_name = "shop.html"

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


class ShopDetailsView(TemplateView):
    template_name = "shop-details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}

        category_and_sub_category['base'] = Category.objects.filter(parent=None)

        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        context['categories_map'] = category_and_sub_category

        return context


class SearchProduct(BaseTemplateView):
    template_name = 'search-product-in-shop.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs['product_id']
        shops_product = ShopProduct.objects.filter(product_id=product_id).order_by('price')

        for i in shops_product:
            i.image = ProductImage.objects.filter(product=i.product).first()
        print(shops_product)
        context['product_shops'] = shops_product
        return context
