import environ
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializer.user_app import (
    CustomTokenObtainPairSerializer,
    ForgotPasswordSerializer,
    PasswordResetConfirmSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UpdatePasswordSerializer,
)
from apps.users.models import User

env = environ.Env()


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token taqdim etilmadi.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Tizimdan muvaffaqiyatli chiqildi!'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'error': "Token yaroqsiz yoki muddati o'tgan."}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ForgotPasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        frontend_url = env('FRONTEND_URL', default='http://localhost:3000')
        reset_link = f'{frontend_url}/reset-password/{uidb64}/{token}/'

        send_mail(
            subject="Parolni tiklash so'rovi",
            message=(
                f"Assalomu alaykum, {user.username}!\n\n"
                f"Parolingizni tiklash uchun:\n{reset_link}\n\n"
                f"Agar bu so'rovni siz yubormagan bo'lsangiz, e'tiborsiz qoldiring."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response({'message': 'Parolni tiklash havolasi emailingizga yuborildi.'}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Parolingiz muvaffaqiyatli yangilandi!'}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = UpdatePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': "Parol muvaffaqiyatli yangilandi!"}, status=status.HTTP_200_OK)
