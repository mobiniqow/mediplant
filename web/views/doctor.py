from abstract_view.base_template_view import BaseTemplateView


class DocktorList(BaseTemplateView):
    template_name = "doctor/doctor-list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
