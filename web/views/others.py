from django.views.generic import TemplateView

from banner.models import Banner
from encyclopedia.models import ArticleEncyclopedia
from product.models import Category, Product, ProductImage
from shop.models import ShopProduct, Shop


class AboutUsView(TemplateView):
    template_name = "about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        context['categories_map'] = category_and_sub_category

        return context


class ContactUsView(TemplateView):
    template_name = "contact-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        context['categories_map'] = category_and_sub_category

        return context
