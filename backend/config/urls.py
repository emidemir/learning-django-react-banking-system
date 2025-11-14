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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.views.generic import TemplateView

# Imports for AUTH
from users.views import CustomUserRegister, CustomUserLogin, google_auth, VerifyAccountAPIView, log_out_user

urlpatterns = [
    # Connecting react with django
    path('', TemplateView.as_view(template_name = 'index.html'), name="index"),

    # Auth URLS
    path('auth/signup/', CustomUserRegister.as_view(), name="user-register"),
    path('auth/login/', CustomUserLogin.as_view(), name="user-login"),
    path('oauth/google/', google_auth, name="google-auth"),
    path('logout/', log_out_user, name="logout"),

    # Admin
    path('admin/', admin.site.urls),

    # Verification code endpoint
    path('verify/', VerifyAccountAPIView.as_view(), name='verify-account'),

    # AllAuth
    path('accounts/', include('allauth.urls')),

    # Profile api
    path('', include('config.routers')),
    
    # JWT views
    path('api/token', TokenObtainPairView.as_view(), name='token-obtain'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token-verify'),

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)