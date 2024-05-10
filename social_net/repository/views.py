import os
import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from .forms import RepositoryCreationForm
from .models import Repository
from social_net import settings



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


def handle_uploaded_file(files, username, repository):
    # Открываем файл для записи на сервере

    files_path = os.path.join(settings.MEDIA_ROOT, 'files')
    os.makedirs(files_path, exist_ok=True)
    files_path = os.path.join(files_path, username)
    os.makedirs(files_path, exist_ok=True)
    files_path = os.path.join(files_path, repository)
    os.mkdir(files_path)

    for file in files:
        with open(os.path.join(files_path, file.name), 'wb+') as destination:
            # Записываем содержимое файла
            for chunk in file.chunks():
                destination.write(chunk)


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
            directories = request.POST['directories']
            handle_uploaded_file(files, repository.user.username, repository.name)
            print(directories)
            # repository.save()
            # messages.success(request, 'Repository created successfully')
            # return redirect('profile', request.user)
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