import os
import shutil
from pathlib import Path

import requests
import json


def upload_file(yandex_token, local_file_path, remote_file_path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {
        'Authorization': yandex_token,
        'Content-Type': 'application/json'
    }
    response = requests.get(url, headers=headers, params={'path': remote_file_path, 'overwrite': True})
    if response.status_code == 200:
        data = json.loads(response.text)
        upload_url = data['href']

        with open(local_file_path, 'rb') as f:
            # Файлы для загрузки
            files = {
                'file': (local_file_path, f, 'multipart/form-data')
            }
            response = requests.put(upload_url, files=files)
            if response.status_code == 201:
                return
            else:
                print(response.status_code)
                print(response.text)
    else:
        print(response.status_code)
        print(response.text)


def make_dir(yandex_token, path):
    url = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        'Authorization': yandex_token,
        'Content-Type': 'application/json'
    }
    response = requests.put(url, headers=headers, params={'path': path})
    if response.status_code == 201:
        data = json.loads(response.text)
        return data
    else:
        print(response.status_code)
        print(response.text)
        raise Exception(response.text)


def upload_folder(yandex_token, path):
    shutil.make_archive(path, 'zip', path)
    try:
        upload_file(yandex_token, path + '.zip', Path(path).name + '.zip')
    except Exception as e:
        print(e)
    finally:
        os.remove(path + '.zip')


# if __name__ == '__main__':
    # yandex_token = 'y0_AgAAAAANpKucAAvNzQAAAAEFLK2qAACRjYZjoPpGTbtzeigOwWzzufl3Hw'
    # # make_dir(yandex_token, 'game/a')
    # # upload_file(yandex_token, "C:/Users/Админ/Downloads/26_demo.txt", "game/26_demo.txt")
    # path = "C:/Users/Админ/Downloads/Telegram Desktop/vkbot"
    # upload_folder(yandex_token, path)