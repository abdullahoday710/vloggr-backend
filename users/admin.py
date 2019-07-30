from django.contrib import admin
from .models import UserProfile, File, FriendNotification
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(File)
admin.site.register(FriendNotification)
