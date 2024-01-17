from django import forms


class VerifyForm(forms.Form):
    phone = forms.CharField(max_length=17)
    code = forms.CharField(max_length=17)
