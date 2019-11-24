import uuid

from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    public_key = models.TextField()
    private_key = models.TextField()
    salt = models.CharField(max_length=250, default=' ')
    iv = models.CharField(max_length=250, default=' ')
    friends = models.ManyToManyField(User, related_name="friendlist")
    invite_code = models.UUIDField()
    profile_picture = models.FileField(blank=True, null=True, default='anon.jpg')
    fcm_token = models.CharField(blank=True,null=True,max_length=255)
    def __str__(self):
        return self.user.username



class FriendNotification(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver")
    accepted = models.BooleanField(default=False)



@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
  if created:
    profile = UserProfile(user=instance, invite_code=uuid.uuid4())
    profile.save()
