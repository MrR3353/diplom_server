from django.urls import path, include
from . import views

urlpatterns = [
    path('upload/<str:temp_repository_name>', views.file_upload_view, name='file_upload_view'),
    path('developers/', views.developers, name='developers'),
    path('create_repository/', views.create_repository, name='create_repository'),
    path('delete_repository/<int:repository_id>', views.delete_repository, name='delete_repository'),
    path('<str:username>/<str:repository_name>', views.repository_detail, name='repository_detail'),
    path('<str:username>/<str:repository_name>/upload', views.api_upload, name='api_upload'),
    path('<str:username>/<str:repository_name>/<str:relative_path>', views.file_detail, name='file_detail'),
    path('<str:username>/', views.profile, name='profile'),
    path('', views.all_repositories, name='all_repositories')
]


