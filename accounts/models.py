from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField(null=True, max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, max_length=250, upload_to="image/", blank=True)
    url_facebook = models.URLField(null=True, max_length=150, blank=True)
    url_twitter = models.URLField(null=True, max_length=150, blank=True)
    phone = models.CharField(max_length=16, null=True, blank=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


