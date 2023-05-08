from django.contrib import admin

from account_module.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(UserLoggedIn)
admin.site.register(UserLoggedOut)
