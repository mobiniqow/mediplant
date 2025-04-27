from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    actions = ['increase_balance', 'decrease_balance', 'reset_balance']

    @admin.action(description="افزایش موجودی کیف پول به مقدار مشخص")
    def increase_balance(self, request, queryset):
        from django import forms
        from django.shortcuts import render, redirect

        class IncreaseForm(forms.Form):
            _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
            amount = forms.IntegerField(label="مقدار افزایش", min_value=1)

        if 'apply' in request.POST:
            form = IncreaseForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                for wallet in queryset:
                    wallet.amount += amount
                    wallet.save()
                self.message_user(request, f"موجودی {queryset.count()} کیف پول با {amount} تومان افزایش یافت.")
                return redirect(request.get_full_path())
        else:
            form = IncreaseForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(request, 'admin/wallet_increase.html', {'form': form, 'wallets': queryset})

    @admin.action(description="کاهش موجودی کیف پول به مقدار مشخص")
    def decrease_balance(self, request, queryset):
        from django import forms
        from django.shortcuts import render, redirect

        class DecreaseForm(forms.Form):
            _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
            amount = forms.IntegerField(label="مقدار کاهش", min_value=1)

        if 'apply' in request.POST:
            form = DecreaseForm(request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                for wallet in queryset:
                    wallet.amount = max(wallet.amount - amount, 0)
                    wallet.save()
                self.message_user(request, f"موجودی {queryset.count()} کیف پول با {amount} تومان کاهش یافت.")
                return redirect(request.get_full_path())
        else:
            form = DecreaseForm(initial={'_selected_action': request.POST.getlist(admin.ACTION_CHECKBOX_NAME)})

        return render(request, 'admin/wallet_decrease.html', {'form': form, 'wallets': queryset})

    @admin.action(description="ریست موجودی کیف پول به صفر")
    def reset_balance(self, request, queryset):
        updated = queryset.update(amount=0)
        self.message_user(request, f"موجودی {updated} کیف پول به صفر ریست شد.")
