from django import forms
from .models import Shop, User

class ShopForm(forms.ModelForm):
    user_name = forms.CharField(max_length=83, label='نام و نام خانوادگی')
    phone = forms.CharField(max_length=17, label='شماره تلفن')
    gender = forms.BooleanField(label='جنسیت')
    national_code = forms.CharField(max_length=10, label='کدملی')
    email = forms.EmailField(label='ایمیل')
    birth_day = forms.DateField(label='تاریخ تولد')
    ref_code = forms.CharField(max_length=8, label='کد معرفی')
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='شهر')
    location = forms.ModelChoiceField(queryset=CityLocation.objects.all(), label='محدوده')
    address = forms.CharField(widget=forms.Textarea, label='آدرس')
    postal_code = forms.CharField(max_length=20, label='کد پستی')

    class Meta:
        model = Shop
        fields = ['name', 'trade_id', 'certificate_image', 'shop_home', 'image', 'mobile', 'description', 'rate_state']

    def save(self, commit=True):
        shop = super().save(commit=False)
        if commit:
            shop.save()

        user_data = {
            'user_name': self.cleaned_data['user_name'],
            'phone': self.cleaned_data['phone'],
            'gender': self.cleaned_data['gender'],
            'national_code': self.cleaned_data['national_code'],
            'email': self.cleaned_data['email'],
            'birth_day': self.cleaned_data['birth_day'],
            'ref_code': self.cleaned_data['ref_code'],
            'city': self.cleaned_data['city'],
            'location': self.cleaned_data['location'],
            'address': self.cleaned_data['address'],
            'postal_code': self.cleaned_data['postal_code'],
        }

        user = User.objects.create(**user_data)
        shop.user = user

        if commit:
            shop.save()

        return shop