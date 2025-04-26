from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from pygments.styles.dracula import comment

from encyclopedia.models import ArticleEncyclopedia, News, Hashtag
from product.models import Category


class EncyclopediaCombinedDrugsView(TemplateView):
    template_name = "article/dorohaie_tarkibi.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        context['categories_map'] = category_and_sub_category
        return context


class EncyclopediaCombinedDetailsView(TemplateView):
    template_name = "article/dorohaie_tarkibi_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        article_id = kwargs['articleId']
        print(article_id)
        context['articleId'] = article_id
        return context


class EncyclopediaView(TemplateView):
    template_name = "article/daneshname_maghalat.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        context['categories_map'] = category_and_sub_category
        return context


class EncyclopediaDetailsView(TemplateView):
    template_name = "article/daneshname_maghalat_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        article_id = kwargs['articleId']
        print(article_id)
        context['articleId'] = article_id

        return context


class DiseasesView(TemplateView):
    template_name = "article/bimariha.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        context['categories_map'] = category_and_sub_category
        return context


class DiseasesDetailsView(TemplateView):
    template_name = "article/bimariha_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        article_id = kwargs['articleId']
        print(article_id)
        context['diseaseId'] = article_id

        return context


class HerbalView(TemplateView):
    template_name = "article/giahan.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        context['categories_map'] = category_and_sub_category
        return context


class HerbalDetailsView(TemplateView):
    template_name = "article/giahan_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        article_id = kwargs['articleId']
        context['articleId'] = article_id
        print(article_id)
        return context


class NewsView(TemplateView):
    template_name = "article/akhbar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        news = News.objects.all().order_by('-id')[:5]
        hashtags = Hashtag.objects.all()
        context['categories_map'] = category_and_sub_category
        context['news'] = news
        context['hashtags'] = hashtags
        return context



class NewsDetailsView(TemplateView):
    template_name = "article/akhbar_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        article_id = kwargs['articleId']
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        news = get_object_or_404(News, id=article_id)
        comments = news.comments.order_by('-id')[:5]
        tags = Hashtag.objects.filter(news=news)
        context['categories_map'] = category_and_sub_category
        context['news'] = news
        context['hashtags'] = tags
        context['comments'] = comments
        context['article_id'] = article_id

        return context
