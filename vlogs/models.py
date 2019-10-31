from django.db import models
from users.models import UserProfile

from jsonfield import JSONField
# Create your models here.
#
class Vlog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    playlist = models.FileField(default="none")
    thumbnail = models.FileField(default="none")
    cipher_object = JSONField(default="none")
    shared_with = models.ManyToManyField(UserProfile, related_name="shared_with",blank=True,null=True)

class Segment(models.Model):
    vlog = models.ForeignKey(Vlog, on_delete=models.CASCADE, related_name="segments")
    file = models.FileField(blank=False, null=False)
