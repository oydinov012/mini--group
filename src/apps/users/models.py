from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phobe_number=models.CharField(max_length=30,blank=True,null=True)
    familiya = models.CharField(max_length=200)

    def __str__(self):
        return self.get_full_name