from django.contrib import admin
from .models import *


class ArticleEncyclopediaCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    list_filter = ('name', 'parent')
    search_fields = ('name',)


admin.site.register(ArticleEncyclopediaCategory, ArticleEncyclopediaCategoryAdmin)
admin.site.register(ArticleReference)


class EncyclopediaArticleInline(admin.TabularInline):
    model = EncyclopediaArticle
    fields = ('reference', 'article')


class ArticleEncyclopediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'registered')
    list_filter = ('name', 'registered')
    inlines = [
        EncyclopediaArticleInline,
    ]
    search_fields = ('name',)


admin.site.register(ArticleEncyclopedia, ArticleEncyclopediaAdmin)


class EncyclopediaCombinedDrugsImageInline(admin.TabularInline):
    model = EncyclopediaCombinedDrugsImage
    fields = ('image',)


class EncyclopediaCombinedDrugsArticleInline(admin.TabularInline):
    model = EncyclopediaCombinedDrugsArticle
    fields = ('article',)


class EncyclopediaCombinedDrugsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ('name',)
    inlines = [
        EncyclopediaCombinedDrugsImageInline,
        EncyclopediaCombinedDrugsArticleInline,
    ]
    search_fields = ('name',)


admin.site.register(EncyclopediaCombinedDrugs, EncyclopediaCombinedDrugsAdmin)


class EncyclopediaOfDiseasesReferenceInline(admin.TabularInline):
    model = EncyclopediaOfDiseasesReference
    fields = ('refrence',)


class EncyclopediaOfDiseasesImageInline(admin.TabularInline):
    model = EncyclopediaOfDiseasesImage
    fields = ('image',)


class EncyclopediaOfDiseasesArticleInline(admin.TabularInline):
    model = EncyclopediaOfDiseasesArticle
    fields = ('article',)


class EncyclopediaOfDiseasesAdmin(admin.ModelAdmin):
    list_display = ('name', 'another_name', 'latin_name', 'cases_of_exacerbation_of_the_disease')
    list_filter = ('name', 'another_name', 'latin_name', 'cases_of_exacerbation_of_the_disease')
    inlines = [
        EncyclopediaOfDiseasesImageInline,
        EncyclopediaOfDiseasesReferenceInline,
        EncyclopediaOfDiseasesArticleInline
    ]
    search_fields = ('name', 'another_name', 'latin_name', 'cases_of_exacerbation_of_the_disease')


admin.site.register(EncyclopediaOfDiseases, EncyclopediaOfDiseasesAdmin)


class HerbalEncyclopediaImageInline(admin.TabularInline):
    model = HerbalEncyclopediaImage
    fields = ('image',)


class HerbalEncyclopediaReferenceInline(admin.TabularInline):
    model = HerbalEncyclopediaReference
    fields = ('refrence',)


class HerbalEncyclopediaArticleInline(admin.TabularInline):
    model = HerbalEncyclopediaArticle
    fields = ('article',)


class HerbalEncyclopediaAdmin(admin.ModelAdmin):
    list_display = ('name', 'another_name', 'latin_name', 'history')
    list_filter = ('name', 'another_name', 'latin_name', 'history')
    inlines = [
        HerbalEncyclopediaImageInline,
        HerbalEncyclopediaReferenceInline,
        HerbalEncyclopediaArticleInline,
    ]
    search_fields = ('name', 'another_name', 'latin_name', 'history')


admin.site.register(HerbalEncyclopedia, HerbalEncyclopediaAdmin)
