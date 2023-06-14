from django.contrib import admin

from contact_module.models import Contact, UnusualContactReason, ContactReport, ContactFormModel

# Register your models here.

admin.site.register(Contact)
admin.site.register(UnusualContactReason)
admin.site.register(ContactReport)
admin.site.register(ContactFormModel)
