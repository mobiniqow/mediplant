from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import get_object_or_404, GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from account.throttles import TwentyPerHourThrottle, FiftyPerDay, SevenPerMinuteThrottle
from account.urls.v1.serializers import (
    VerifySerializer,
    ProfileSerializer,
    UserRegisterSerializer,
    LoginSerializer,
    GeneralSerializer,
    TokenSerializer,
)
from rest_framework.views import APIView
from account.send_sms import send_otp_message
from rest_framework import status
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from random import randint
from datetime import timedelta
from django.core.mail import send_mail


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class ProfileAPIView(APIView):  # تنها کاربران وارد شده می‌توانند از این API استفاده کنند

    def get(self, request):
        """
        دریافت اطلاعات پروفایل کاربر وارد شده
        """

        user = request.user  # دسترسی به کاربر جاری
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        """
        به روز رسانی اطلاعات جزئی پروفایل کاربر
        """
        user = request.user  # دسترسی به کاربر جاری
        # فرض بر این است که در فرم داده‌های PATCH فقط فیلدهای خاص ارسال می‌شود
        serializer = ProfileSerializer(user, data=request.data,
                                       partial=True)  # `partial=True` برای اجازه دادن به به‌روزرسانی جزئی

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyAPIView(GenericAPIView):
    serializer_class = VerifySerializer
    throttle_classes = [SevenPerMinuteThrottle, TwentyPerHourThrottle, FiftyPerDay]

    @swagger_auto_schema(
        responses={200: TokenSerializer(many=True), 404: GeneralSerializer()}
    )
    def post(self, request):
        """
        verify user phone by sending otp code
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        user = get_object_or_404(User, phone=phone)
        if user.check_password(serializer.validated_data.get("password")):
            user.state = User.State.ACTIVE
            user.phone_is_verify = True
            user.save()
            serializer = TokenSerializer(get_tokens_for_user(user))
            return Response(serializer.data)
        else:
            serializer = GeneralSerializer({"message": "wrong code"})
            return Response(serializer.data, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    throttle_classes = [SevenPerMinuteThrottle, TwentyPerHourThrottle, FiftyPerDay]

    @swagger_auto_schema(responses={200: GeneralSerializer()})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(**serializer.data)
        otp = User.objects.make_random_password(length=4, allowed_chars="123456789")
        send_otp_message(user.phone, otp)
        user.set_password(otp)
        user.save()
        serializer = GeneralSerializer({"message": "code sending to your phone"})
        return Response(serializer.data)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer
    throttle_classes = [SevenPerMinuteThrottle, TwentyPerHourThrottle, FiftyPerDay]

    @swagger_auto_schema(responses={200: GeneralSerializer()})
    def post(self, request):
        """
        login user by phone number
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data.get("phone")
        user = get_object_or_404(User, phone=phone)

        otp = User.objects.make_random_password(length=4, allowed_chars="123456789")
        user.set_password(otp)
        send_otp_message(phone, otp)
        user.save()
        serializer = GeneralSerializer({"message": "code sending to your phone"})
        return Response(serializer.data)


class SendPhoneOtpAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        if not phone:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        # تولید OTP
        otp = ''.join([str(randint(0, 9)) for _ in range(4)])
        user = request.user

        if not user:
            return Response({"error": "User with this phone number does not exist."}, status=status.HTTP_404_NOT_FOUND)
        user.phone = phone
        user.phone_otp = otp
        user.phone_otp_sent_at = timezone.now()
        user.phone_is_verify = False
        user.save()

        # ارسال OTP به شماره تلفن (با Twilio یا روش‌های دیگر)
        send_sms(phone, otp)

        return Response({"message": "OTP sent to phone number."}, status=status.HTTP_200_OK)


class SendEmailOtpAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # تولید OTP
        otp = ''.join([str(randint(0, 9)) for _ in range(4)])
        user = request.user

        if not user:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # ذخیره OTP در مدل
        user.email = email
        user.email_otp = otp
        user.email_otp_sent_at = timezone.now()
        user.email_is_verify = False
        user.save()

        # ارسال OTP به ایمیل
        send_mail(
            user.email,
            otp,
        )

        return Response({"message": "OTP sent to email."}, status=status.HTTP_200_OK)


class VerifyPhoneOtpAPIView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        otp = request.data.get('otp')

        if not phone or not otp:
            return Response({"error": "Phone number and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone=phone).first()

        if not user:
            return Response({"error": "User with this phone number does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # بررسی OTP
        if user.phone_otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی زمان انقضا (مثلاً 10 دقیقه)
        otp_sent_time = user.phone_otp_sent_at
        if timezone.now() - otp_sent_time > timedelta(minutes=10):
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # تغییر وضعیت تایید شماره تلفن
        user.phone_is_verify = True
        user.save()

        return Response({"message": "Phone number verified successfully."}, status=status.HTTP_200_OK)


class VerifyEmailOtpAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        if not user:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # بررسی OTP
        if user.email_otp != otp:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

        # بررسی زمان انقضا (مثلاً 10 دقیقه)
        otp_sent_time = user.email_otp_sent_at
        if timezone.now() - otp_sent_time > timedelta(minutes=10):
            return Response({"error": "OTP has expired"}, status=status.HTTP_400_BAD_REQUEST)

        # تغییر وضعیت تایید ایمیل
        user.email_is_verify = True
        user.save()

        return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)


def send_sms(phone, otp):
    print(otp)


def send_mail(phone, otp):
    print(otp)
