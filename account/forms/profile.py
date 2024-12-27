from django import forms
from account.models import User
from city.models import City, CityLocation


class ProfileForm(forms.ModelForm):
    # specify the name of model to use

    class Meta:
        model = User
        fields = (
            # 'avatar',
            'user_name',
            'phone',
            'gender',
            'email',
            'city',
            # 'location',
            'address',
            'postal_code',
        )
        widgets = {
            'city': forms.Select(attrs={'class': 'form-drop-down'}),
        }