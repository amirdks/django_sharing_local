from django.contrib import admin

from account_module.models import User, UserLoggedOut, AdministrativeDepartment, UserLoggedIn, \
    AdministrativeDepartmentHead

# Register your models here.
admin.site.register(User)
admin.site.register(UserLoggedIn)
admin.site.register(UserLoggedOut)
admin.site.register(AdministrativeDepartment)
admin.site.register(AdministrativeDepartmentHead)
