from django.contrib.auth.models import User
from django.db import models

from userdashboard.choices import USER_ROLE_CHOICES


class ApplicationUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    university = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True, choices=USER_ROLE_CHOICES, default='USER')

    def __str__(self):
        return self.user.username
