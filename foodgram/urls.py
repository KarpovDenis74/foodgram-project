"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# from django import urls
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from recipes import views
from rest_framework.routers import DefaultRouter





urlpatterns = [
    path('api/v1/ingredients/', views.RecipeViewList.as_view(),
         name="api_ingredients"),
    path('admin/', admin.site.urls),
    path('users/', include("users.urls")),
    path('recipes/', include("recipes.urls")),
    path('', views.RecipeViewList.as_view(), name="index"),
]
