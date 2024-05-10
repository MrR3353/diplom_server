import os
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RepositoryCreationForm
from .models import Repository


def profile(request, username):
    user = get_object_or_404(User, username=username)
    repositories = Repository.objects.all().filter(user=user)
    default_profile_images = os.listdir('../social_net/account/static/images/default_profile_images')
    # default_profile_image = default_profile_images[user.id % len(default_profile_images)]
    default_profile_image = random.choice(default_profile_images)
    if user == request.user:
        return render(request, 'repository/profile.html',
                      {'section': 'profile', 'repositories': repositories, 'author': user, 'default_profile_image': default_profile_image})
    else:
        return render(request, 'repository/profile.html',
                      {'repositories': repositories, 'author': user, 'default_profile_image': default_profile_image})


def all_repositories(request):
    repositories = Repository.objects.all()
    return render(request, 'repository/all_repositories.html',
                  {'section': 'all_repositories', 'repositories': repositories})


@login_required
def create_repository(request):
    if request.method == 'POST':
        form = RepositoryCreationForm(request.POST, user=request.user)
        if form.is_valid():
            repository = Repository(
                name=request.POST['name'],
                description=request.POST['description'],
                user=request.user  # Указываем текущего пользователя
            )
            repository.save()
            messages.success(request, 'Repository created successfully')
            return redirect('profile', request.user)
        else:
            messages.error(request, 'Error creating new repository')
    else:
        form = RepositoryCreationForm(user=request.user)
    return render(request, 'repository/create_repository.html', {'form': form})


@login_required
def repository_detail(request, username, repository_name):
    user = get_object_or_404(User, username=username)
    repository = get_object_or_404(Repository, user=user, name=repository_name)
    return render(request, 'repository/repository_detail.html', {'repository': repository})


def people(request):
    users = User.objects.all()
    return render(request, 'repository/people.html', {'section': 'people', 'users': users})