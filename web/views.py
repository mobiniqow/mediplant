from django.views.generic import TemplateView

from banner.models import Banner


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        banners = Banner.objects.filter(state=Banner.State.ACTIVE).order_by('?')[:6]
        print(len(banner))
        # banners =
        context['title'] = 'صفحه اصلی'
        context['title'] = 'صفحه اصلی'
        context['banner'] = banners
        return context
