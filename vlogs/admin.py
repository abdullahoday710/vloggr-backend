from django.contrib import admin
from .models import Vlog, Segment, Album
# Register your models here.
admin.site.register(Segment)
admin.site.register(Album)

class VlogAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)

admin.site.register(Vlog, VlogAdmin)
