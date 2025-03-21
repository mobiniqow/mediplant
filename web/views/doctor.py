from django.shortcuts import get_object_or_404, redirect

from abstract_view.base_template_view import BaseTemplateView
from doctor.models import Doctor
from doctor_visit.models import DoctorVisit, DoctorVisitChat
from transaction.models import DoctorTransaction


class DoctorList(BaseTemplateView):
    template_name = "doctor/doctor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DoctorDetailsList(BaseTemplateView):
    template_name = "doctor/doctor_details.html"

    def dispatch(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctor, pk=kwargs['doctor'])

        # چک کردن وضعیت پرداخت و هدایت به صفحه چت در صورت تأیید تراکنش
        if DoctorVisit.objects.filter(
                user=self.request.user,
                doctor=doctor,
                transaction__transaction_type=DoctorTransaction.TransactionState.ACCEPT
        ).exists():
            return redirect(f"/medicine/{doctor.id}/chats/")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = get_object_or_404(Doctor, pk=kwargs['doctor'])
        visits = DoctorVisit.objects.filter(doctor_id=doctor, state=DoctorVisit.State.DoctorEnd).count()

        context['doctor'] = doctor
        context['visits'] = visits
        return context


class DoctorChatDetails(BaseTemplateView):
    template_name = "doctor/chats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = kwargs['doctor']
        doctor = get_object_or_404(Doctor, pk=doctor)
        visits = DoctorVisit.objects.filter(doctor_id=doctor, state=DoctorVisit.State.DoctorEnd).count()
        chats = DoctorVisitChat.objects.filter(doctor__doctor=doctor)
        for i in chats:
            i.is_read = 'true' if i.is_read else 'false'
            i.is_doctor = 'true' if i.is_doctor else 'false'
            if i.media:
                i.media_url = i.media.url
            else:
                i.media_url = ""
        print(f'chats {chats.count()}')
        context['doctor'] = doctor
        context['visits'] = visits
        context['chats'] = chats
        return context


class DoctorprescriptionDetails(BaseTemplateView):
    template_name = "doctor/prescription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = kwargs['doctor']
        doctor = get_object_or_404(Doctor, pk=doctor)
        visits = DoctorVisit.objects.filter(doctor_id=doctor, state=DoctorVisit.State.DoctorEnd).count()
        context['doctor'] = doctor

        context['visits'] = visits

        return context


class DoctorHistoryDetails(BaseTemplateView):
    template_name = "doctor/doctor_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = kwargs['doctor']
        doctor = get_object_or_404(Doctor, pk=doctor)
        visits = DoctorVisit.objects.filter(doctor_id=doctor, state=DoctorVisit.State.END).count()
        context['doctor'] = doctor

        context['visits'] = visits

        return context
