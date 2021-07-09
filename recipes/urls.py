from django.urls import path
# from django.urls.conf import include
from recipes import views


urlpatterns = [
    path('', views.index, name="index"),
]
