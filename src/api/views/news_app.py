from rest_framework import viewsets
from api.serializer.news_app import NewsTypeSerializer, NewsSerializer, NewsImageSrializer  
from apps.news.models import NewsType, News, NewsImage
from api.paginations import CustomPagination

class  NewsTypeView(viewsets.ReadOnlyModelViewSet):

    queryset= NewsType.objects.all()
    serializer_class = NewsTypeSerializer



class NewsView(viewsets.ReadOnlyModelViewSet):

    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        queryset = self.queryset
        type_id = self.request.query_params.get('type')
        if type_id is not None:
            queryset = queryset.filter(news_type_id=type_id)
        return queryset
