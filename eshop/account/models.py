from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50, default='', blank=True)
    reset_password_expire = models.DateTimeField(null=True, blank=True)


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    user = instance
    print('inctance', instance)
    if created:
        profile = Profile(user = user)
        profile.save()