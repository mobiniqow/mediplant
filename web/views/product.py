from abstract_view.base_template_view import BaseTemplateView
from product.models import Product, ProductImage
from shop.models import ShopProduct


class ShopProductView(BaseTemplateView):
    template_name = 'product-details.html'

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
