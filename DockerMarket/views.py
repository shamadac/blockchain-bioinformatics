# Import Django modules

from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from bigchaindb_driver.crypto import generate_keypair
from hashlib import sha256


from .models import Docker, User, RegistrationForm, DockerSubmissionForm

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

def user_detail_view(request, pk):
    template = 'DockerMarket/user_detail_view.html'
    user = get_object_or_404(User, pk=pk)
    
    context = {
            'user': user,
            }
    
    return render(request, template, context)

def new_user_view(request):
    template = 'DockerMarket/new_user_view.html'
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()
            return redirect('DockerMarket:user_view', pk=new_user.pk)

    else:
        form = RegistrationForm()
    
    context = {
            'form': form,
            }
    
    return render(request, template, context)


def new_docker_view(request):
    template = 'DockerMarket/new_docker_view.html'
    if request.method == "POST":
        form = DockerSubmissionForm(request.POST, request.FILES)
        
        if form.is_valid():
            new_docker = form.save(commit=False)
            new_docker.save()
            
            return redirect('DockerMarket:docker_view', slug=new_docker.slug)
    else:
        form = DockerSubmissionForm()
    
    context = {
            'form': form,
            }
    
    return render(request, template, context)