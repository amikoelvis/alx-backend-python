"""
URL configuration for messaging_app project.

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
from django.urls import path, include  # include is required

urlpatterns = [
    path('admin/', admin.site.urls),

    # All chats API endpoints now live under /api/
    path('api/', include('chats.urls')),

    # Add DRF's browsable API login/logout
    path('api-auth/', include('rest_framework.urls')),
]

# api-auth/ should be included so you can use Django REST Framework’s built-in authentication views (login/logout for the browsable API).