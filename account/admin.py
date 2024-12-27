from django.contrib import admin

from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'phone', 'email', 'is_staff']
    list_filter = ['state', 'activation_state', 'gender']
    search_fields = ['user_name', 'phone', 'email']
    # اضافه کردن فیلدهای مرتبط به صورت اینلاین
    inlines = []

admin.site.register(User, UserAdmin)
