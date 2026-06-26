from rest_framework import serializers
from apps.news.models import News, NewsImage, NewsType

class NewsImageSrializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image']


class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSrializer(many=True, read_only=True)
    class Meta:
        model = News
        fields = ['id', 'news_type', 'title', 'description', 'cover_image', 'images', 'is_published', 'created_at', 'updated_at']


class NewsTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsType
        fields = ['id', 'name']