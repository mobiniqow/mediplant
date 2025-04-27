from rest_framework_simplejwt.tokens import RefreshToken
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
from sale.models import SaleBasket
from product.models import Category
from encyclopedia.models import ArticleEncyclopedia, News, Hashtag


class LoginView(BaseTemplateView):
    template_name = "account/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                return redirect('/verify/' + form.cleaned_data['phone'])
            else:
                print("else form.is_valid()")
                return self.form_invalid(form)
        else:
            print(f'request.user.state = {request.user.state }')
            print(f'User.State.GUEST = {User.State.GUEST }')
            if request.user.state != User.State.GUEST:
                return redirect('/')
            context = self.get_context_data()
            login = LoginForm()
            context['form'] = login
        return self.render_to_response(context)

    def form_valid(self, form):
        user = User.objects.filter(phone=form.cleaned_data['phone'])
        if user.exists():
            user = user.first()
            if user.role is not User.Role.USER:
                from django.http import Http404
                raise Http404("صفحه مورد نظر یافت نشد")

        else:
            serializer = UserRegisterSerializer(data=form.cleaned_data)
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
    template_name = "account/verify.html"

    def post(self, request, *args, **kwargs):
        form = VerifyForm(request.POST)
        if form.is_valid():
            user = User.objects.get(phone=form.cleaned_data['phone'])
            if user.check_password(form.cleaned_data['code']):
                user.state = User.State.ACTIVE
                user.save()
                session_key = self.request.session.session_key or self.request.META.get('REMOTE_ADDR')
                basket = SaleBasket.objects.filter(session_key=session_key, state__lte=SaleBasket.State.IN_PAY)
                login(request, user)
                for i in basket:
                    i.user = request.user
                    i.session_key = None
                    i.save()
                return redirect("/")
        context = self.get_context_data(form=form)
        context['error'] = "کد صحیح نمیباشد"
        return self.render_to_response(context)

    def dispatch(self, request, *args, **kwargs):
        if request.user.state != User.State.GUEST:
            return redirect('/')
        return super().dispatch(request, *args, **kwargs)


class ProfileView(BaseTemplateView):
    template_name = "account/profile.html"

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

            # Create JWT token for the authenticated user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)  # Get the access token as string
            context['user'] = request.user
            context['token'] = access_token  # Pass the JWT token to the context

            profile = ProfileForm(instance=user)
            context['form'] = profile

        return self.render_to_response(context)
class Tickets(BaseTemplateView):
    template_name = "account/ticket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        news = News.objects.all().order_by('-id')[:5]
        hashtags = Hashtag.objects.all()
        context['categories_map'] = category_and_sub_category
        context['news'] = news
        context['hashtags'] = hashtags
        return context
class NewTicket(BaseTemplateView):
    template_name = "account/new_ticket.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        news = News.objects.all().order_by('-id')[:5]
        hashtags = Hashtag.objects.all()
        context['categories_map'] = category_and_sub_category
        context['news'] = news
        context['hashtags'] = hashtags
        return context
class TicketHistory(BaseTemplateView):
    template_name = "account/ticket_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_and_sub_category = {}
        category_and_sub_category['base'] = Category.objects.filter(parent=None)
        for i in category_and_sub_category['base']:
            i.children = Category.objects.filter(parent=i.id)
        news = News.objects.all().order_by('-id')[:5]
        hashtags = Hashtag.objects.all()
        context['categories_map'] = category_and_sub_category
        context['news'] = news
        context['hashtags'] = hashtags
        return context