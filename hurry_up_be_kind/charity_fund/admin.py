from django.contrib import admin
from .models import UserData



class UserDataAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserData, UserDataAdmin)

