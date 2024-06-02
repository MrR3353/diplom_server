from django.db import models
from django.contrib.auth.models import User
from repository.models import Repository


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    repository = models.ForeignKey(Repository, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Order of {self.user.username} on {self.repository.name}'
