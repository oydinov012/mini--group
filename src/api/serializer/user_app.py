from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    tokens = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'photo', 'tokens')

    def get_tokens(self, obj):
        return obj.token()

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            phone=validated_data.get('phone', None),
            photo=validated_data.get('photo', None)
        )
        return user
    



class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        
        data['user'] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
            "phone": self.user.phone,
            "photo": self.user.photo.url if self.user.photo else None
        }
        return data
    


from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

User = get_user_model()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Bu email manzili bilan foydalanuvchi topilmadi.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=6)

    def validate(self, attrs):
        try:
            # uidb64 dan foydalanuvchi ID sini qayta tiklaymiz
            uid = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"token": "Yaroqsiz havola yoki foydalanuvchi topilmadi."})

        # Token xavfsizligini va muddati o'tmaganini tekshiramiz
        if not default_token_generator.check_token(user, attrs['token']):
            raise serializers.ValidationError({"token": "Token yaroqsiz yoki muddati o'tgan."})

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        # Yangi parolni xavfsiz (hash) ko'rinishda saqlaymiz
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    



