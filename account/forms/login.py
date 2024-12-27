from django import forms
from account.models import User


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=17)

