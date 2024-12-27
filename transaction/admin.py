from django.contrib import admin

from transaction.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'state', 'created_at']
    list_filter = ['state']
    readonly_fields = ['created_at']

    class Meta:
        model = Transaction