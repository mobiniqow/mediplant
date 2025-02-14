from django.views.generic import TemplateView

from product.models import Category


class AboutUsView(TemplateView):
    template_name = "shop/about-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        context['categories_map'] = category_and_sub_category

        return context


class ContactUsView(TemplateView):
    template_name = "shop/contact-us.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        context['categories_map'] = category_and_sub_category

        return context
