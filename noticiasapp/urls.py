from django.urls import path
from . import views

urlpatterns = [
    path('', views.g1_news, name='g1_news'),
]
