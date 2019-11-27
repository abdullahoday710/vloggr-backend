from django.contrib import admin
from .models import UserProfile, FriendNotification, User
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(FriendNotification)
admin.site.register(User)
