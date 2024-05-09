from django.urls import path, include
from . import views

urlpatterns = [
    path('create_repository/', views.create_repository, name='create_repository'),
    path('people/', views.people, name='people'),
    path('<str:username>/<str:repository_name>', views.repository_detail, name='repository_detail'),
    path('<str:username>/', views.user_repositories, name='user_repositories'),
    path('', views.all_repositories, name='all_repositories'),
]