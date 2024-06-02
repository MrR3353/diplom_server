from django.contrib.auth.models import User
from django.db import models


class Repository(models.Model):
    PUBLIC = 'public'
    PRIVATE = 'private'
    PAID = 'paid'

    REPOSITORY_TYPES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (PAID, 'Paid'),
    ]

    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    type = models.CharField(
        max_length=10,
        choices=REPOSITORY_TYPES,
        default=PUBLIC,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f'Repository {self.name}'
