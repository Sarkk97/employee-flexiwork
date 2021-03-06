"""flexiwork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from users.views import MyTokenObtainPairView

urlpatterns = [
    path('api/v1/docs/openapi', get_schema_view(
        title="Flexiwork",
        description="Energy360 Africa Flexiwork API …",
        version="1.0.0",
    ), name='openapi-schema'),
    path('api/v1/docs', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url':'openapi-schema'}),
        name='redoc'),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('clocking.urls'))
]
