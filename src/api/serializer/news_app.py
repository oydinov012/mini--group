from rest_framework.serializers import ModelSerializer
from apps.news.models import NewsType, News, NewsImage


class NewsTypeSerializer(ModelSerializer):
    class Meta:
        model = NewsType
        fields = '__all__'


class NewsImageSerializer(ModelSerializer):
    class Meta:
        model = NewsImage
        fields = '__all__'


class NewsSerializer(ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)

    class Meta:
        model = News
        fields = '__all__'