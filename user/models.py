
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, null=True)
    phone = models.CharField(max_length=18, unique=True, null=True)
    user_name = models.CharField(max_length=100, unique=True, null=True)
    profile_image = models.CharField(max_length=200, null=True)
    token = models.CharField(max_length=200, null=True)
    date_joined = models. DateTimeField(auto_now_add=True, null=True)
    data_updated = models. DateTimeField(auto_now=True, null=True)

    # thumbnail set shavad badan
    def __str__(self):
        return self.email



class VerifyPassword(models.Model):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=18, null=True)
    code = models.CharField(max_length=10)
    time_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.email