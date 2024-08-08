from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse

from abstract_view.base_template_view import BaseTemplateView
from account.forms.login import LoginForm
from account.forms.profile import ProfileForm
from account.forms.verify import VerifyForm
from account.models import User
from account.send_sms import send_otp_message
from account.urls.v1.serializers import UserRegisterSerializer


class LoginView(BaseTemplateView):
    template_name = "login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            if request.user.is_authenticated:
                return redirect('/')
            context = self.get_context_data()
            login = LoginForm()
            context['form'] = login
        return self.render_to_response(context)

    def form_valid(self, form):
        user = User.objects.filter(phone=form.cleaned_data['phone'])
        if user.exists():
            user = user.first()
        else:
            serializer = UserRegisterSerializer(data=form.cleaned_data)
            print(f'create new user ')
            if not serializer.is_valid():
                context = self.get_context_data(form=form)
                context['error'] = "شماره تلفن اشتباه وارد شده"
                return self.render_to_response(context)
            user = User(**serializer.data)
        otp = User.objects.make_random_password(length=4, allowed_chars="123456789")
        send_otp_message(user.phone, otp)
        user.set_password(otp)
        user.save()
        verify_url = reverse('verify', kwargs={'phone': user.phone})

        return redirect(verify_url)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['error'] = "شماره را درست وارد کنید."
        return self.render_to_response(context)


class VerifyView(BaseTemplateView):
    template_name = "verify.html"

    def post(self, request, *args, **kwargs):
        form = VerifyForm(request.POST)
        if form.is_valid():
            user = User.objects.get(phone=form.cleaned_data['phone'])
            if user.check_password(form.cleaned_data['code']):
                user.state = User.State.ACTIVE
                user.save()
                login(request, user)
                return redirect("/")
        context = self.get_context_data(form=form)
        context['error'] = "کد صحیح نمیباشد"

        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        context = self.get_context_data()
        return self.render_to_response(context)


class ProfileView(BaseTemplateView):
    template_name = "account/profile.html"

    # def post(self, request, *args, **kwargs):
    #     print(21)
    #     form = ProfileForm(request.POST, instance=request.user)
    #     if form.is_valid():
    #         form.save()
    #         return redirect("/")
    #     context = self.get_context_data(form=form)
    #     context['form'] = form
    #     return self.render_to_response(context)

    #
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            context = self.get_context_data()
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return self.render_to_response(context)
            else:
                context['form'] = form
                return self.render_to_response(context)
        else:
            user = request.user
            context = self.get_context_data()
            profile = ProfileForm(instance=user)
            context['form'] = profile
        return self.render_to_response(context)
