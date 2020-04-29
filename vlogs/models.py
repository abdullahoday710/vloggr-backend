from django.db import models
from users.models import UserProfile

from jsonfield import JSONField

class UserCipher(models.Model):
    email = models.CharField(max_length=100)
    cipher = models.CharField(max_length=200)

class Album(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.email + " - {}".format(self.name)


class Vlog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    playlist = models.FileField(default="none")
    thumbnail = models.FileField(default="none")
    user_ciphers = models.ManyToManyField(UserCipher, related_name="shared_with_data")
    shared_with = models.ManyToManyField(UserProfile, related_name="shared_with",blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.user.email + "'s vlog object (pk {})".format(self.pk)


class Photo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    user_ciphers = models.ManyToManyField(UserCipher, related_name="photo_shared_with_data")
    shared_with = models.ManyToManyField(UserProfile, related_name="photo_shared_with",blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(default="none")
    iv = models.CharField(max_length=70)
    def __str__(self):
        return self.user.user.email + "'s photo object (pk {})".format(self.pk)


class Segment(models.Model):
    vlog = models.ForeignKey(Vlog, on_delete=models.CASCADE, related_name="segments")
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.vlog.user.user.email + "'s vlog segment (pk {})".format(self.pk)
