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


def get_file_structure(repo_path, relative_path):
    full_path = os.path.join(repo_path, relative_path)
    file_structure = {'dir': Path(full_path).name, 'path': relative_path, 'files': [], 'subdir': []}
    for item in os.listdir(full_path):
        relative_item_path = os.path.join(relative_path, item)
        absolute_item_path = os.path.join(repo_path, relative_item_path)
        if os.path.isfile(absolute_item_path):
            file_structure['files'].append({'name': item, 'path': relative_item_path})
        elif os.path.isdir(absolute_item_path):
            file_structure['subdir'].append(get_file_structure(repo_path, relative_item_path))
    return file_structure


def get_file_type(file_path):
    # Получаем расширение файла
    file_extension = os.path.splitext(file_path)[1].lower()
    text_extensions = ['.txt', '.py', '.java', '.cpp', '.c', '.html', '.css', '.js', '.xml', '.json', '.md', '.csv',
                       '.log', '.php', '.rb', '.pl', '.sql', '.yaml', '.yml', '.ini', '.cfg', '.conf', '.sh', '.bat',
                       '.cmd', '.ps1', '.psm1', '.psd1', '.ps1xml', '.psc1', '.pssc', '.h', '.hpp', '.hxx', '.m', '.mm',
                       '.phps', '.php3', '.php4', '.php5', '.phtml', '.ctp', '.jinja', '.twig', '.coffee', '.scss',
                       '.less', '.jsx', '.tsx', '.vue', '.php', '.html', '.htm', '.tpl', '.phtml', '.inc', '.asp',
                       '.aspx', '.ascx', '.ashx', '.asmx', '.asax', '.cs', '.cshtml', '.vb', '.master', '.sitemap',
                       '.webinfo', '.config', '.appconfig', '.ini', '.inf', '.reg', '.htaccess', '.htpasswd', '.conf',
                       '.log', '.svg', '.json', '.xml', '.yml', '.yaml', '.md', '.rst', '.csv', '.sql', '.bak', '.swp',
                       '.tmp', '.temp', '.lock', '.thumbs.db', '.desktop.ini', '.suo', '.sln', '.vcproj', '.cproject',
                       '.dir-locals.el', '.project', '.classpath', '.settings', '.properties', '.ini', '.yaml', '.yml',
                       '.toml', '.xml', '.json', '.yml', '.yaml', '.env']  # и т.д.
    img_extensions = ['.jpg', '.png', '.gif', '.bmp', '.tiff', '.svg', '.webp']  # и т.д.

    if file_extension in text_extensions:
        return 'text'
    elif file_extension in img_extensions:
        return 'img'
    else:
        return None

# def get_file_structure(directory):
#     file_structure = {'dir': Path(directory).name, 'path': directory, 'files': [], 'subdir': []}
#     for item in os.listdir(directory):
#         item_path = os.path.join(directory, item)
#         if os.path.isfile(item_path):
#             file_structure['files'].append({'name': item, 'path': item_path})
#         elif os.path.isdir(item_path):
#             file_structure['subdir'].append(get_file_structure(item_path))
#     return file_structure
