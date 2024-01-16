from django.views.generic import TemplateView

from banner.models import Banner
from encyclopedia.models import ArticleEncyclopedia
from product.models import Category, Product, ProductImage
from shop.models import ShopProduct, Shop


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):

        return context
