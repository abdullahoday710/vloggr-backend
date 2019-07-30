from django.db import models
from users.models import UserProfile

from jsonfield import JSONField
# Create your models here.
#
class Vlog(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    file = models.FileField(blank=False, null=False)
    thumbnail = models.FileField()
    cipher_object = JSONField()
