from django.contrib import admin

from banner.models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['name', 'image','type', 'state']
    search_fields = ['name', 'link_url','type']
    list_editable = ('state','type')
