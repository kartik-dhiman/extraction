from django.contrib import admin

from .models import UserRequest, CrawledUrls


class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'input_url', '_fetched_url_count')
    list_filter = ('user', 'created_at')
    list_per_page = 20


class CrawledUrlsAdmin(admin.ModelAdmin):
    list_display = ('user_request', 'created_at', 'shortUrl', 'is_processed')
    list_filter = ('user_request', 'created_at')
    list_per_page = 20


admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(CrawledUrls, CrawledUrlsAdmin)
