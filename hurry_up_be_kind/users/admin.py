from django.contrib import admin
from .models import UserData, AvatarUser



class UserDataAdmin(admin.ModelAdmin):
    pass

class AvatarUserAdmin(admin.ModelAdmin):
    pass



admin.site.register(UserData, UserDataAdmin)
admin.site.register(AvatarUser, AvatarUserAdmin)