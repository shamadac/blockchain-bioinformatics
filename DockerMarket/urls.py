# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'DockerMarket'
urlpatterns = [
    path('', views.dockermarket_home_view, name='home'),
    path('dockers/<slug>/', views.docker_detail_view, name='docker_view'),
    path('users/<int:pk>/', views.user_detail_view, name='user_view'),
    path('submit-docker/', views.new_docker_view, name='new_docker_view'),
    path('register/', views.new_user_view, name='new_user_view'),
]