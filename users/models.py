from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from bcrypt import gensalt
from django.contrib.postgres.fields import JSONField
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField()
    private_key = models.TextField()
    salt = models.CharField(max_length=250, default=' ')
    iv = models.CharField(max_length=250, default=' ')
    friends = models.ManyToManyField(User, related_name="friendlist")
    def __str__(self):
        return self.user.username

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    def __str__(self):
        return self.file.name



class FriendNotification(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver")
    accepted = models.BooleanField(default=False)









@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
  if created:
    profile = UserProfile(user=instance)
    profile.save()
