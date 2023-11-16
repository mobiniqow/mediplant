from django.shortcuts import render
from .forms import ShopForm

def index(request):
    if request.method == 'POST':
        form = ShopForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # انجام دیگر عملیات مورد نیاز
    else:
        form =ShopForm(request.POST, request.FILES)
    return render(request, 'indexx.html', {'form': form})