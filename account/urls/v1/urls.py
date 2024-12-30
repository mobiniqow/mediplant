from django.urls import path
from account.urls.v1.views import (
    RegisterAPIView,
    LoginAPIView,
    ProfileAPIView,
    VerifyAPIView,
    SendPhoneOtpAPIView,
    SendEmailOtpAPIView,
    VerifyPhoneOtpAPIView,
    VerifyEmailOtpAPIView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from rest_framework_simplejwt.views import TokenVerifyView

app_name = "v1"
urlpatterns = [
    path("verify/", VerifyAPIView.as_view(), name="verify"),
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("register/", RegisterAPIView.as_view(), name="register"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("is-verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('send-phone-otp/', SendPhoneOtpAPIView.as_view(), name='send-phone-otp'),
    path('send-email-otp/', SendEmailOtpAPIView.as_view(), name='send-email-otp'),
    path('verify-phone-otp/', VerifyPhoneOtpAPIView.as_view(), name='verify-phone-otp'),
    path('verify-email-otp/', VerifyEmailOtpAPIView.as_view(), name='verify-email-otp'),

]
