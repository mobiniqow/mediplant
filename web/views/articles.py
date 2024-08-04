from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404

from encyclopedia.models import ArticleEncyclopedia
from product.models import Category


class BlogsView(TemplateView):
    template_name = "blogs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)

        context['categories_map'] = category_and_sub_category

        return context


class BlogsDetailsView(TemplateView):
    template_name = "blog-detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        obj_id = kwargs['id']

        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        obj = get_object_or_404(ArticleEncyclopedia, pk=obj_id)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        recent_article = ArticleEncyclopedia.objects.all().order_by('id')[:5]
        context['categories_map'] = category_and_sub_category
        context['recent_article'] = recent_article
        context['item'] = obj

        return context

