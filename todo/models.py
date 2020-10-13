from django.conf import settings
from django.db import models


class Task(models.Model):  # Table name, has to wrap models.Model to get the functionality of Django.

    title = models.CharField(max_length=200)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    description = models.TextField()

    def __str__(self):
        self.done = False
        return self.title
