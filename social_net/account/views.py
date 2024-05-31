import json
import os

from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from . import yandex_api
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from social_net import settings


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request,
#                                 username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login or password')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})


def logout_view(request):
    logout(request)
    # return redirect('login') # на главную страницу сайта
    return render(request, 'registration/logged_out.html')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создать новый объект пользователя, но пока не сохранять его
            new_user = user_form.save(commit=False)
            # Установить выбранный пароль
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохранить объект User
            new_user.save()
            # Создать профиль пользователя
            Profile.objects.create(user=new_user)
            login(request, new_user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('all_repositories')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@csrf_exempt
@login_required
def yandex(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        access_token = data.get('access_token')
        user = get_object_or_404(User, username=request.user.username)
        user.profile.yandex_token = access_token
        user.profile.save()
        return JsonResponse({'message': 'OK'})
    return JsonResponse({'message': 'Method not allowed'}, status=405)


@login_required
def yandex_upload(request, username, repository_name):
    yandex_api.upload_folder(request.user.profile.yandex_token, os.path.join(settings.MEDIA_ROOT, 'files', username, repository_name))
    messages.success(request, 'Repository uploaded to Yandex disc')
    return redirect('repository_detail', username, repository_name)

