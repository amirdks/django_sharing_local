from django.contrib import admin
from .models import Birthday, Event, File, HyperLink

# Register your models here.

admin.site.register(Birthday)
admin.site.register(Event)
admin.site.register(File)
admin.site.register(HyperLink)
