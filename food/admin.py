from django.contrib import admin
from django.utils.safestring import mark_safe
from urllib.parse import quote
from .models import *


@admin.register(Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']


@admin.register(Shop)
class AdminShop(admin.ModelAdmin):
    list_display = ['category', 'name', 'address_link']
    list_display_links = ['name']
    search_fields = ['category']

    def address_link(self, shop):
        if shop.address:
            url = 'https://map.naver.com/?query=' + quote(shop.address)
            return mark_safe('<a href="{}" target="_blank">{}</a>'.format(url, shop.address))
        return None

    address_link.short_description = '주소 (네이버 지도)'
