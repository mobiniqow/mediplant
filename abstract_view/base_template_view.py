from django.views.generic import TemplateView

from product.models import Category


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
        if self.request.user :
            from account.urls.v1.views import get_tokens_for_user
            token = get_tokens_for_user(self.request.user)
            context['token'] = token['access']
            print(token['access'])
        else:
            context['token'] = ""
        context['categories'] = categories
        if context['is_active']:
            # todo ino ok konam shomareshshesho
            context['medic_notification'] = 0
            context['shop_notification'] = 4

            # context['']
        return context