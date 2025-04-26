from django.contrib import admin
from .models import UserRefLogs,UserActivateLogs
class UserRefLogsAdmin(admin.ModelAdmin):
    list_display = ['ref', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['ref__user_name', 'user__user_name']

admin.site.register(UserRefLogs, UserRefLogsAdmin)


class UserActivateLogsAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__user_name']

admin.site.register(UserActivateLogs, UserActivateLogsAdmin)