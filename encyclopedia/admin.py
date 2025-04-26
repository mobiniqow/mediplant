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

# news
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
    fields = ['user_name', 'email', 'message', 'status', 'created_at']
    readonly_fields = ['created_at']
    autocomplete_fields = ['parent_comment']


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'status', 'created_at', 'news_title')  # ستونی برای نمایش در لیست کامنت‌ها
    list_filter = ('status', 'created_at', 'news')  # فیلتر بر اساس وضعیت، تاریخ و خبر مرتبط
    search_fields = ('user_name', 'email', 'message')  # امکان جستجو بر اساس نام کاربر، ایمیل و پیام
    actions = ['set_status_active', 'set_status_inactive']  # امکان تغییر وضعیت به صورت جمعی
    list_per_page = 20  # تعداد نمایش هر صفحه در لیست کامنت‌ها

    def news_title(self, obj):
        return obj.news.title  # نمایش عنوان خبر مرتبط با کامنت

    news_title.admin_order_field = 'news__title'  # امکان مرتب‌سازی بر اساس عنوان خبر

    def set_status_active(self, request, queryset):
        queryset.update(status='active')  # تغییر وضعیت کامنت‌ها به فعال
        self.message_user(request, "وضعیت کامنت‌ها به 'فعال' تغییر کرد.")

    set_status_active.short_description = "تغییر وضعیت به 'فعال'"

    def set_status_inactive(self, request, queryset):
        queryset.update(status='inactive')  # تغییر وضعیت کامنت‌ها به غیرفعال
        self.message_user(request, "وضعیت کامنت‌ها به 'غیرفعال' تغییر کرد.")

    set_status_inactive.short_description = "تغییر وضعیت به 'غیرفعال'"


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at', 'hashtag_list')  # فیلدهای نمایش داده شده در لیست اخبار
    search_fields = ('title', 'content')  # جستجو بر اساس عنوان و محتوا
    list_filter = ('created_at', 'updated_at', 'hashtags')  # فیلتر بر اساس تاریخ و هشتگ‌ها
    inlines = [CommentInline]  # نمایش کامنت‌ها به صورت اینلاین در بخش خبر
    list_per_page = 20  # تعداد نمایش هر صفحه در لیست اخبار

    def hashtag_list(self, obj):
        return ", ".join([hashtag.name for hashtag in obj.hashtags.all()])  # نمایش هشتگ‌های مرتبط با خبر

    hashtag_list.short_description = "هشتگ‌ها"


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Hashtag, HashtagAdmin)
