from django.contrib import admin
from .models import Transaction, Payment
from sale.models import SaleBasket

# Custom admin for the Transaction model
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'status', 'timestamp', 'authority', 'message','cart')
    list_filter = ('transaction_type', 'status', 'timestamp','cart')
    search_fields = ('user__user_name', 'status', 'transaction_type', 'amount')
    ordering = ('-timestamp',)
    date_hierarchy = 'timestamp'
    # You can add additional filter options like `date_hierarchy`, etc. if needed

    def save_model(self, request, obj, form, change):
        # Optional: Add custom save logic if needed
        super().save_model(request, obj, form, change)

# Custom admin for the Payment model
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'cart', 'status', 'created_at', 'payment_url')
    list_filter = ('status', 'created_at')
    search_fields = ('user__user_name', 'cart__id', 'payment_url')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        # Optional: Add custom save logic if needed
        super().save_model(request, obj, form, change)

# Register your models with custom admins
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Payment, PaymentAdmin)
