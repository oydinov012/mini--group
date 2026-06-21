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
        fields = ['id', 'title', 'images', 'content', 'created_at']


class NewsTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewsType
        fields = ['id', 'name']


