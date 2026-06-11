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