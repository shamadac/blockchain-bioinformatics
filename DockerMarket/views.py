# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Docker, User

def dockermarket_home_view(request):
    template = 'DockerMarket/dockermarket_home_view.html'
    docker_list = Docker.objects.all()
    context = {
            'docker_list': docker_list,
            }
    return render(request, template, context)


def docker_detail_view(request, slug):
    template = 'DockerMarket/docker_detail_view.html'
    docker = get_object_or_404(Docker, slug=slug)
    
    context = {
            'docker': docker,
            }
    
    return render(request, template, context)