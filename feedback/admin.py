from django.contrib import admin
from .models import FeedbackCart, FeedbackObject

@admin.register(FeedbackCart)
class FeedbackCartAdmin(admin.ModelAdmin):
    list_display = ('cart', 'state', 'created_at', 'is_feedback_sent', 'slug')
    list_filter = ('state', 'is_feedback_sent', 'created_at')
    search_fields = ('slug', 'cart__user__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(FeedbackObject)
class FeedbackObjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

