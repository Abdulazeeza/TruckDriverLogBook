"""
URL configuration for truck_driver_log_book project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from urllib.parse import urlparse

def get_base_domain(url):
    if settings.APP_ENV in ['local']:
        return url
    
    parsed_url = urlparse(url)
    return parsed_url.netloc

SCHEME = 'http' if settings.APP_ENV in ['local'] else 'https'

schema_view = get_schema_view(
    openapi.Info(
        title="Truck Driver Log Book API",
        default_version='v1',
        description="This documents contains all the endpoints available for truck driver log book Frontend to call",
        terms_of_service="",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    url=f"{SCHEME}://{get_base_domain(settings.APP_URL)}",
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = DefaultRouter()


swagger_routes = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.user_app.urls')),
    path('api/', include(router.urls)),
] + swagger_routes
