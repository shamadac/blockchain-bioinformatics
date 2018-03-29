# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'DockerMarket'
urlpatterns = [
    path('', views.dockermarket_home_view, name='home'),
    path('<slug>/', views.docker_detail_view, name='docker_view'),  
]