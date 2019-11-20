from django.contrib import admin
from .models import Vlog, Segment, Album, Photo
# Register your models here.
admin.site.register(Segment)
admin.site.register(Album)
admin.site.register(Photo)
class VlogAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

admin.site.register(Vlog, VlogAdmin)
