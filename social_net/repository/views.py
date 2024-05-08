from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def my_repositories(request):
    repositories = []
    return render(request, 'repository/dashboard.html', {'repositories': repositories})


# @login_required
# def create_repository(request):
#     if request.
    # repositories = []
    # return render(request, 'repository/dashboard.html', {'repositories': repositories})