import datetime
import io
import json
import os
import random
import shutil
import string
import time
import zipfile
from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse, Http404, FileResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import RepositoryCreationForm
from .models import Repository
from .file_handlers import save_uploaded_files, get_file_structure, get_file_type, detect_encoding, \
    get_human_readable_size
from social_net import settings
from payment.models import Order


def developers(request):
    users = User.objects.all()
    return render(request, 'repository/developers.html', {'section': 'developers', 'users': users})


def all_repositories(request):
    repositories = Repository.objects.all()
    for i in range(len(repositories)):
        if repositories[i].user == request.user or Order.objects.filter(user=request.user.id, repository=repositories[i], paid=True):
            repositories[i].available = True
        else:
            repositories[i].available = False
    return render(request, 'repository/all_repositories.html',
                  {'section': 'all_repositories', 'repositories': repositories})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    repositories = Repository.objects.all().filter(user=user)
    default_profile_images = os.listdir('../social_net/account/static/images/default_profile_images')
    # default_profile_image = default_profile_images[user.id % len(default_profile_images)]
    default_profile_image = random.choice(default_profile_images)
    for i in range(len(repositories)):
        if repositories[i].user == request.user or Order.objects.filter(user=request.user, repository=repositories[i], paid=True):
            repositories[i].available = True
        else:
            repositories[i].available = False

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
    if repository.type == Repository.PRIVATE and request.user != repository.user:
        raise Http404("Repository does not exist")
    elif repository.type == Repository.PAID and request.user != repository.user:
        orders = Order.objects.filter(user=request.user, repository=repository, paid=True)
        if not orders:
            return render(request, 'repository/repository_buy.html', {'repository': repository})
    return render(request, 'repository/repository_detail.html', {'repository': repository, 'file_structure': file_structure})


@login_required
def create_repository(request):
    # TODO: не загружает пустые папки
    if request.method == 'POST':
        form = RepositoryCreationForm(request.POST, user=request.user)
        if form.is_valid():
            repository = Repository(
                name=request.POST['name'],
                description=request.POST['description'],
                type=request.POST['type'],
                price=request.POST['price'],
                user=request.user  # Указываем текущего пользователя
            )
            files = request.FILES.getlist('files')
            if len(files) > 0:
                full_paths = request.POST['directories']
                full_paths = json.loads(full_paths)
                assert len(files) == len(full_paths)
                for i in range(len(files)):
                    save_uploaded_files([files[i]], {files[i].name: full_paths[i]}, repository.user.username, repository.name)
            else:
                temp_repository_name = request.POST['temp_repository_name']
                full_path_temp_repository = os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, temp_repository_name)
                if os.path.exists(full_path_temp_repository):
                    os.rename(full_path_temp_repository, os.path.join(settings.MEDIA_ROOT, 'files', request.user.username, repository.name))
            repository.save()
            messages.success(request, 'Repository created successfully')
            return redirect('repository_detail', repository.user.username, repository.name)
        else:
            messages.error(request, 'Error creating new repository')
    else:
        form = RepositoryCreationForm(user=request.user)
    temp_repository_name = 'tmp_' + str(datetime.date.today()) + '_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5))
    return render(request, 'repository/create_repository.html', {'form': form, 'temp_repository_name': temp_repository_name})


@login_required()
def file_upload_view(request, temp_repository_name):
    """
    Сохраняет файл с помощью save_uploaded_files в media
    Относительные пути удаляет браузер или Django, поэтому их передаем с помощью JS
    в словаре full_paths в виде {"имя_файла": "относительный_путь_файла"}
    :return:
    """
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        if files:
            full_paths = request.POST['full_paths']
            full_paths = json.loads(full_paths)
            save_uploaded_files(files, full_paths, request.user.username, temp_repository_name)
            return JsonResponse({'message': f'Файл {full_paths[files[0].name]} загружен успешно!'})
        else:
            return JsonResponse({'message': 'Нет файлов'})
    return render(request, 'repository/upload.html')


@csrf_exempt
def api_upload(request, username, repository_name):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        repository = get_object_or_404(Repository, user=user, name=repository_name)
        token = request.POST['token']
        if user.profile.token != token:
            return JsonResponse({'message': 'Invalid token'}, status=401)
        path = request.POST['path']
        file = request.FILES.get('file')
        if file:
            save_uploaded_files([file], {file.name: path}, username, repository_name)
            return JsonResponse({'message': 'Ok', 'file': file.name, 'path': path})
        else:
            return JsonResponse({'message': 'Нет файла'}, status=400)
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def api_download(request, username, repository_name):
    if request.method == 'GET':
        user = get_object_or_404(User, username=username)
        repository = get_object_or_404(Repository, user=user, name=repository_name)
        # token = request.GET.get('token')
        # if user.profile.token != token:
        #     return JsonResponse({'message': 'Invalid token'}, status=401)
        full_path = os.path.join(settings.MEDIA_ROOT, 'files', username, repository_name)
        if not os.path.exists(full_path):
            return JsonResponse({'message': 'Folder not exists'}, status=404)

        # Create a zip file in memory
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, full_path)
                    zip_file.write(file_path, arcname)
        zip_buffer.seek(0)

        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(full_path)}.zip'
        return response
    return JsonResponse({'message': 'Method not allowed'}, status=405)


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
    return redirect('repository_detail', repository.user.username, repository.name)


def file_detail(request, username, repository_name, relative_path):
    relative_path = Path(relative_path)
    absolute_path = os.path.join(settings.MEDIA_ROOT, 'files', username, repository_name, relative_path)
    if not os.path.exists(absolute_path):
        raise Http404(f"File {relative_path} not found")

    user = get_object_or_404(User, username=username)
    repository = get_object_or_404(Repository, user=user, name=repository_name)

    if repository.type == Repository.PRIVATE and request.user != repository.user:
        raise Http404("Repository does not exist")
    elif repository.type == Repository.PAID and request.user != repository.user:
        orders = Order.objects.filter(user=request.user, repository=repository, paid=True)
        if not orders:
            return render(request, 'repository/repository_buy.html', {'repository': repository})

    if os.path.isdir(absolute_path):
        repo_path = os.path.join(settings.MEDIA_ROOT, 'files', repository.user.username, repository.name)
        file_structure = get_file_structure(repo_path, relative_path)
        return render(request, 'repository/repository_detail.html',
                      {'repository': repository, 'file_structure': file_structure})
    else:
        text_lines = None
        img_path = None
        file_type = get_file_type(relative_path)
        file_info = os.stat(absolute_path)
        if file_type == 'text':
            with open(absolute_path, 'r', encoding=detect_encoding(absolute_path)) as file:
                text_lines = file.readlines()
        elif file_type == 'img':
            img_path = os.path.join('files', username, repository_name, relative_path)
        return render(request, 'repository/file_detail.html', {
                          'repository': repository,
                          'relative_path': relative_path,
                          'text_lines': text_lines,
                          'img_path': img_path,
                          'file_size': get_human_readable_size(file_info.st_size),
                          'last_modified': time.ctime(file_info.st_mtime),
        })




