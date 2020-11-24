from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):  # Table name, has to wrap models.Model to get the functionality of Django.

    title = models.CharField(max_length=200)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    done = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        self.done = False
        return self.title
