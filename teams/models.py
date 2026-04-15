from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    skills = models.TextField(blank=True)
    dependencies = models.TextField(blank=True)

    def __str__(self):
        return self.name
