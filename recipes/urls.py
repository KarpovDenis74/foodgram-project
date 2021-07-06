from django.urls import path
from django.urls.conf import include
from recipes import views


urlpatterns = [
    path('index/', views.index, name="index"),
]
