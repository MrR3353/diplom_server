# .
# ├── account
# │   ├── static
# │   │   └── css
# │   │       └── base.css
# │   ├── templates
# │   │   ├── account
# │   │   │   └── profile.html
# │   │   ├── registration
# │   │   │   ├── logged_out.html
# │   │   │   ├── login.html
# │   │   │   ├── password_change_done.html
# │   │   │   ├── password_change_form.html
# │   │   │   ├── password_reset_complete.html
# │   │   │   ├── password_reset_confirm.html
# │   │   │   ├── password_reset_done.html
# │   │   │   ├── password_reset_email.html
# │   │   │   └── password_reset_form.html
# │   │   └── base.html
# │   ├── admin.py
# │   ├── apps.py
# │   ├── forms.py
# │   ├── __init__.py
# │   ├── models.py
# │   ├── tests.py
# │   ├── urls.py
# │   └── views.py
# ├── bookmarks
# │   ├── asgi.py
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   └── wsgi.py
# ├── db.sqlite3
# ├── manage.py
# └── README.md
import datetime
import json
import os
import shutil

from pathlib import Path

from django.core.files.uploadedfile import UploadedFile

# cd .\social_net\
# python manage.py runserver


# for m in range(0, 30, 2):
#     for n in range(1, 29, 2):
#         N = 2**m * 3**n
#         if 200_000_000 <= N <= 400_000_000:
#             print(N)
# print(a)
# import math
#
# print(math.log2(400_000_000))
# print(2**28)

# for i in range(200_000_000, 400_000_000 + 1):
#     a = i
#     n, m = 0, 0
#     while a % 3 == 0:
#         a //= 3
#         n += 1
#     while a % 2 == 0:
#         a //= 2
#         m += 1
#     if a == 1 and m % 2 == 0 and n % 2 != 0:
#         print(i)

# s = '{"17.txt":"В3_04052024_файлы/17.txt","18.xls":"В3_04052024_файлы/18.xls","22.xlsx":"В3_04052024_файлы/22.xlsx","24.txt":"В3_04052024_файлы/24.txt","26.txt":"В3_04052024_файлы/26.txt","27_A.txt":"В3_04052024_файлы/27_A.txt","27_B.txt":"В3_04052024_файлы/27_B.txt","3.xlsx":"В3_04052024_файлы/3.xlsx","9.xlsx":"В3_04052024_файлы/9.xlsx","Куприн Александр. Поединок.docx":"В3_04052024_файлы/Куприн Александр. Поединок.docx"}'
# directories = json.loads(s)
# print(directories)

# os.makedirs('__MACOSX/._В3_04052024.pdf', exist_ok=True)
# os.makedirs('a/b/c/d/e.py', exist_ok=True)
# shutil.rmtree('a/b')


# a = '["Достоевский/17.txt","Достоевский/Идиот.htm","Достоевский/Идиот.pdf","Достоевский/Идиот.rtf","Достоевский/Преступление и наказание.pdf","Достоевский/Преступление и наказание.txt","Достоевский/Новая папка/17.txt","Достоевский/Новая папка/Идиот.htm","Достоевский/Новая папка/Идиот.pdf"]'
# directories = json.loads(a)
# print(directories[0])
import random, string

print(str(datetime.date.today()) + '_' + ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(5)))
