from django.contrib import admin

from contact_module.models import Contact, UnusualContactReason

# Register your models here.

admin.site.register(Contact)
admin.site.register(UnusualContactReason)
