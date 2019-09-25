from django.db import models
from users.models import UserProfile

from jsonfield import JSONField
# Create your models here.
#
class Vlog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    playlist = models.FileField(blank=False, null=False)
    thumbnail = models.FileField()
    cipher_object = JSONField()

class Segment(models.Model):
    vlog = models.ForeignKey(Vlog, on_delete=models.CASCADE, related_name="segments")
    file = models.FileField(blank=False, null=False)
