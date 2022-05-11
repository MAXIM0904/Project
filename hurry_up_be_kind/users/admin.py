from django.contrib import admin
from .models import UserData, AvatarUser


class AvatarUserAdmin(admin.ModelAdmin):
    pass


class AdminAvatarUser(admin.TabularInline):
    model = AvatarUser


class UserDataAdmin(admin.ModelAdmin):
    inlines = [
        AdminAvatarUser,
    ]


admin.site.register(UserData, UserDataAdmin)
admin.site.register(AvatarUser, AvatarUserAdmin)
