from django.contrib import admin

from banner.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'link_url', ]
    search_fields = ['name', 'link_url']
