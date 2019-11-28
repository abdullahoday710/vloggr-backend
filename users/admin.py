from django.contrib import admin
from .models import UserProfile, FriendNotification, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Register your models here.

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'is_active', 'is_staff')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(UserProfile)
admin.site.register(FriendNotification)
admin.site.register(User, UserAdmin)
