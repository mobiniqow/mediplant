from abstract_view.base_template_view import BaseTemplateView
from product.models import Product, ProductImage
from shop.models import ShopProduct
from django.shortcuts import get_object_or_404


class ShopProductView(BaseTemplateView):
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = kwargs['product_id']
        product_shops: ShopProduct = get_object_or_404(ShopProduct, id=product_id, )
        products = Product.objects.select_related('class_id', 'category', 'unit').prefetch_related('images')[:10]
        product_shops.image = ProductImage.objects.filter(product=product_id)
        for i in products:
            i.image_list = i.images.all()
        context['products'] = products
        context['product_shops'] = product_shops
        context['images'] = product_shops.image
        return context


class ShopProductListView(BaseTemplateView):
    template_name = 'product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_shops = get_object_or_404(ShopProduct)
        products = Product.objects.select_related('class_id', 'category', 'unit').prefetch_related('images')[:10]
        product_shops.image = ProductImage.objects.filter(product=product_id)
        for i in products:
            i.image_list = i.images.all()
        context['products'] = products
        context['product_shops'] = product_shops
        context['images'] = product_shops.image
        return context
