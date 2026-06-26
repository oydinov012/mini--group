from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response
from api.serializer.news_app import NewsTypeSerializer, NewsSerializer, NewsImageSrializer  
from apps.news.models import NewsType, News, NewsImage
from api.paginations import CustomPagination


class NewsTypeView(viewsets.ReadOnlyModelViewSet):
    queryset = NewsType.objects.all()
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


# ── Admin CRUD ────────────────────────────────────────────────────────────────

class NewsAdminListCreateView(generics.ListCreateAPIView):
    queryset = News.objects.all().order_by('-created_at')
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = self.queryset
        type_id = self.request.query_params.get('type')
        if type_id:
            qs = qs.filter(news_type_id=type_id)
        is_pub = self.request.query_params.get('is_published')
        if is_pub is not None:
            qs = qs.filter(is_published=is_pub.lower() == 'true')
        return qs


class NewsAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer
    permission_classes = [IsAdminUser]


class NewsTypeAdminListCreateView(generics.ListCreateAPIView):
    queryset = NewsType.objects.all()
    serializer_class = NewsTypeSerializer
    permission_classes = [IsAdminUser]


class NewsTypeAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsType.objects.all()
    serializer_class = NewsTypeSerializer
    permission_classes = [IsAdminUser]


class NewsImageAdminListCreateView(generics.ListCreateAPIView):
    serializer_class = NewsImageSrializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return NewsImage.objects.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(news_id=self.kwargs['news_id'])


class NewsImageAdminDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsImage.objects.all()
    serializer_class = NewsImageSrializer
    permission_classes = [IsAdminUser]