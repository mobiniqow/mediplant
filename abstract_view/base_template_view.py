from django.views.generic import TemplateView
from django.contrib.auth import login
from account.models import User
# from account.models import User, GuestUser
from product.models import Category
from sale.models import SaleBasket


class BaseTemplateView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        category_and_sub_category['user'] = self.request.user
        context['categories_map'] = category_and_sub_category
        context['is_active'] = self.request.user is not None
        categories = Category.objects.filter(parent=None)

        if not self.request.user.is_authenticated:
            session_key = self.request.session.session_key or self.request.META.get('REMOTE_ADDR')
            basket = SaleBasket.objects.filter(session_key=session_key, state__lte=SaleBasket.State.IN_PAY)
        else:
            basket = SaleBasket.objects.filter(user=self.request.user, state__lte=SaleBasket.State.IN_PAY)
        context['basket'] = basket
        print(f'self.request.user.id {basket}')
        if self.request.user.id is not None:
            from account.urls.v1.views import get_tokens_for_user
            token = get_tokens_for_user(self.request.user)
            context['token'] = token['access']
            print(token['access'])
        else:
            from account.urls.v1.views import get_tokens_for_user
            guest_user = User.objects.create_guest_user()
            guest_user.save()
            guest_token = get_tokens_for_user(guest_user)
            context['token'] = guest_token['access']
            login(self.request, guest_user)
        context['categories'] = categories
        if context['is_active']:
            # todo ino ok konam shomareshshesho
            context['medic_notification'] = 0
            context['shop_notification'] = len(basket)

            # context['']
        return context
