import json
import os
import random
import shutil
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import RepositoryCreationForm
from .models import Repository
from .file_handlers import save_uploaded_files, get_file_structure, get_file_type
from social_net import settings


def developers(request):
    users = User.objects.all()
    return render(request, 'repository/developers.html', {'section': 'developers', 'users': users})


def all_repositories(request):
    repositories = Repository.objects.all()
    return render(request, 'repository/all_repositories.html',
                  {'section': 'all_repositories', 'repositories': repositories})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    repositories = Repository.objects.all().filter(user=user)
    default_profile_images = os.listdir('../social_net/account/static/images/default_profile_images')
    # default_profile_image = default_profile_images[user.id % len(default_profile_images)]
    default_profile_image = random.choice(default_profile_images)
    if user == request.user:
        return render(request, 'repository/profile.html',
                      {'section': 'profile', 'repositories': repositories, 'author': user,
                       'default_profile_image': default_profile_image})
    else:
        return render(request, 'repository/profile.html',
                      {'repositories': repositories, 'author': user, 'default_profile_image': default_profile_image})


@login_required
def repository_detail(request, username, repository_name):
    user = get_object_or_404(User, username=username)
    repository = get_object_or_404(Repository, user=user, name=repository_name)
    repo_path = os.path.join(settings.MEDIA_ROOT, 'files', repository.user.username, repository.name)
    file_structure = None
    if os.path.exists(repo_path):
        file_structure = get_file_structure(repo_path, '')
    return render(request, 'repository/repository_detail.html', {'repository': repository, 'file_structure': file_structure})


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
            files = request.FILES.getlist('files')
            if len(files) > 0:
                full_path = request.POST['directories']
                save_uploaded_files(files, full_path, repository.user.username, repository.name)
            repository.save()
            messages.success(request, 'Repository created successfully')
            return redirect('profile', request.user)
        else:
            messages.error(request, 'Error creating new repository')
    else:
        form = RepositoryCreationForm(user=request.user)
    return render(request, 'repository/create_repository.html', {'form': form})


@login_required()
def delete_repository(request, repository_id):
    repository = get_object_or_404(Repository, pk=repository_id)
    if request.user == repository.user:
        repository.delete()
        repo_path = os.path.join(settings.MEDIA_ROOT, 'files', repository.user.username, repository.name)
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        messages.success(request, 'Repository deleted successfully')
        return redirect('profile', request.user)
    messages.error(request, 'You do not have permission to delete that repository')
    return redirect('repository_detail', repository.name)


def file_detail(request, username, repository_name, relative_path):
    relative_path = Path(relative_path)
    absolute_path = os.path.join(settings.MEDIA_ROOT, 'files', username, repository_name, relative_path)
    text_lines = None
    if get_file_type(relative_path) == 'text':
        try:
            with open(absolute_path, 'r', encoding='utf-8') as file:
                text_lines = file.readlines()
        except UnicodeDecodeError as e:
            with open(absolute_path, 'r') as file:
                text_lines = file.readlines()
    return render(request, 'repository/file_detail.html', {'relative_path': relative_path, 'text_lines': text_lines})