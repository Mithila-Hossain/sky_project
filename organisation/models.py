# Author: Bernard Vecino w19733959

from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    specialisation = models.CharField(max_length=100, blank=True)
    head = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="departments_led")

    def __str__(self):
        return self.name
