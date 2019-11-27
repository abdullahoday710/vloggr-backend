import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import ugettext_lazy as _

class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    public_key = models.TextField()
    private_key = models.TextField()
    salt = models.CharField(max_length=250, default=' ')
    iv = models.CharField(max_length=250, default=' ')
    friends = models.ManyToManyField(User, related_name="friendlist")
    invite_code = models.UUIDField()
    profile_picture = models.FileField(blank=True, null=True, default='anon.jpg')
    fcm_token = models.CharField(blank=True,null=True,max_length=255)
    def __str__(self):
        return self.user.email



class FriendNotification(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="receiver")
    accepted = models.BooleanField(default=False)



@receiver(post_save, sender=User)
def build_profile_on_user_creation(sender, instance, created, **kwargs):
  if created:
    profile = UserProfile(user=instance, invite_code=uuid.uuid4())
    profile.save()
