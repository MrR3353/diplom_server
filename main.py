# .
# ├── account
# │   ├── static
# │   │   └── css
# │   │       └── base.css
# │   ├── templates
# │   │   ├── account
# │   │   │   └── my_repositories.html
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
from functools import lru_cache


# cd .\social_net\
# python manage.py runserver

# print((25 ** 0.5) % 1)


def moves(k):
    return k + 1, k + 4, k * 5

@lru_cache(None)
def game(k):
    if k >= 68: return 'W'
    if any(game(x) == 'W' for x in moves(k)): return 'W1'
    if all(game(x) == 'W1' for x in moves(k)): return 'W2'
    if any(game(x) == 'W2' for x in moves(k)): return 'W3'
    if all(game(x) == 'W3' or game(x) == 'W1' for x in moves(k)): return 'W4'


for s in range(1, 80):
    if game(s) == 'W4':
        print(s)



