from django.urls import path, include
from . import views

urlpatterns = [
    path('create_repository/', views.create_repository, name='create_repository'),
    path('developers/', views.developers, name='developers'),
    path('delete_repository/<int:repository_id>', views.delete_repository, name='delete_repository'),
    path('<str:username>/<str:repository_name>', views.repository_detail, name='repository_detail'),
    path('<str:username>/<str:repository_name>/<str:relative_path>', views.file_detail, name='file_detail'),
    path('<str:username>/', views.profile, name='profile'),
    path('', views.all_repositories, name='all_repositories')
]


