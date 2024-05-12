import json
import os
import shutil
from pathlib import Path

from social_net import settings


def save_uploaded_files(files, full_path, username, repository):
    # TODO: не загружает папку .vcs и файл README.md который лежит в папке
    # преобразуем строку в dict
    full_path = json.loads(full_path)
    files_path = os.path.join(settings.MEDIA_ROOT, 'files')
    os.makedirs(files_path, exist_ok=True)
    user_path = os.path.join(files_path, username)
    os.makedirs(user_path, exist_ok=True)
    repo_path = os.path.join(user_path, repository)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        os.mkdir(repo_path)

    for file in files:
        file_path = os.path.split(full_path[file.name])
        os.makedirs(os.path.join(repo_path, *file_path[:-1]), exist_ok=True)
        with open(os.path.join(repo_path, *file_path), 'wb+') as destination:
            # Записываем содержимое файла
            for chunk in file.chunks():
                destination.write(chunk)


def get_file_structure(directory):
    file_structure = {'dir': Path(directory).name, 'files': [], 'subdir': []}
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isfile(item_path):
            file_structure['files'].append(item)
        elif os.path.isdir(item_path):
            file_structure['subdir'].append(get_file_structure(item_path))
    return file_structure

