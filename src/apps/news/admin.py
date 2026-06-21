from django.contrib import admin
from apps.news.models import News  , NewsType  , NewsImage

admin.site.register(News)
admin.site.register(NewsType)
admin.site.register(NewsImage)