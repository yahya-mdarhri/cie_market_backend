"""
URL configuration for config project.

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
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from accounts.views import HomeView
from rest_framework_simplejwt.authentication import JWTAuthentication
from accounts.authentication import TokenAuthentication

schema_view = get_schema_view(
    openapi.Info(
        title="CIE Inventor Platform API",
        default_version='v1.0',
        description="API documentation for the CIE Inventors, Tickets, Patents, and affiliations.",
        # terms_of_service="https://www.example.com/terms/",
        # contact=openapi.Contact(email="support@example.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=False,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(TokenAuthentication,),
)

urlpatterns = [
    
    # API endpoints
    # path('', HomeView.as_view({'get': 'retrieve'}), name='home'),
    path('api/accounts/', include('accounts.urls')),
    path('api/inventors/', include('inventors.urls')),


    # API docs URLs
    # re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc',  cache_timeout=0), name='schema-redoc'),
]
