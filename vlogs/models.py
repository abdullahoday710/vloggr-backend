from django.db import models
from users.models import UserProfile

from jsonfield import JSONField
# Create your models here.

class Album(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username + " - {}".format(self.name)


class Vlog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    playlist = models.FileField(default="none")
    thumbnail = models.FileField(default="none")
    cipher_object = JSONField(default="none")
    shared_with = models.ManyToManyField(UserProfile, related_name="shared_with",blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.user.username + "'s vlog object (pk {})".format(self.pk)

class Segment(models.Model):
    vlog = models.ForeignKey(Vlog, on_delete=models.CASCADE, related_name="segments")
    file = models.FileField(blank=False, null=False)

    def __str__(self):
        return self.vlog.user.user.username + "'s vlog segment (pk {})".format(self.pk)
