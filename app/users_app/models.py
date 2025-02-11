from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
#     timezone = models.CharField(max_length=100)


class CustomGroup(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.CharField(max_length=255, null=True)
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.group.name
