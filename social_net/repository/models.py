from django.contrib.auth.models import User
from django.db import models


class Repository(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'Repository {self.name}'
