from django.contrib import admin

from feedback.models import FeedBackShop, FeedBackDoctorVisit


@admin.register(FeedBackShop)
class FeedBackShopAdmin(admin.ModelAdmin):
    list_display = ['id', 'shop', 'state', 'comment', 'rate', 'created_at']
    list_filter = ['state', 'created_at']
    search_fields = ['shop__name']
    list_per_page = 20

    class Meta:
        model = FeedBackShop
        verbose_name = 'بازخورد فروشگاه'
        verbose_name_plural = 'بازخوردهای فروشگاه'


@admin.register(FeedBackDoctorVisit)
class FeedBackDoctorVisitAdmin(admin.ModelAdmin):
    list_display = ['id', 'visit', 'state', 'comment', 'rate', 'created_at']
    list_filter = ['state', 'created_at']
    search_fields = ['visit__doctor__doctor__user__name']
    list_per_page = 20

    class Meta:
        model = FeedBackShop
        verbose_name = 'بازخورد فروشگاه'
        verbose_name_plural = 'بازخوردهای فروشگاه'
