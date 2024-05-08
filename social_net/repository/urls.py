from django.urls import path, include
from . import views

urlpatterns = [
    path('my/', views.my_repositories, name='my_repositories'),
]