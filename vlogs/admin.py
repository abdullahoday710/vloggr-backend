from django.contrib import admin
from .models import Vlog, Segment, Album, Photo, UserCipher
# Register your models here.
admin.site.register(Segment)
admin.site.register(Album)
admin.site.register(Photo)
admin.site.register(UserCipher)
class VlogAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

admin.site.register(Vlog, VlogAdmin)
