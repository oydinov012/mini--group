
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include
from .views import home_page
urlpatterns = [
    path('',home_page, name='home'),

    
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),

    # documentatsiya uchun
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]







