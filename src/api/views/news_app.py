from rest_framework import generics
from rest_framework.permissions import IsAdminUser, AllowAny
from apps.news.models import NewsType, News, NewsImage
from api.serializer.news_app import NewsTypeSerializer, NewsSerializer, NewsImageSerializer
from api.paginations import CustomPagination


class NewsTypeListCreateView(generics.ListCreateAPIView):
    queryset = NewsType.objects.filter(is_active=True)
    serializer_class = NewsTypeSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class NewsTypeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsType.objects.all()
    serializer_class = NewsTypeSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class NewsListCreateView(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = News.objects.filter(is_published=True).select_related('news_type').prefetch_related('images')
        if self.request.query_params.get('type'):
            qs = qs.filter(news_type_id=self.request.query_params['type'])
        return qs

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class NewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all().prefetch_related('images')
    serializer_class = NewsSerializer

    def get_permissions(self):
        return [AllowAny()] if self.request.method == 'GET' else [IsAdminUser()]


class NewsImageListCreateView(generics.ListCreateAPIView):
    serializer_class = NewsImageSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return NewsImage.objects.filter(news_id=self.kwargs['news_id'])

    def perform_create(self, serializer):
        serializer.save(news_id=self.kwargs['news_id'])


class NewsImageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = NewsImage.objects.all()
    serializer_class = NewsImageSerializer
    permission_classes = [IsAdminUser]