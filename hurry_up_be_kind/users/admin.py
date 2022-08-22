from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from .process import _sending_sms
from .models import UserData, FileUser


class FileUserAdmin(admin.ModelAdmin):
    list_display = ('model_file', 'file_user', )
    search_fields = ('file_user',)


class AdminFileUser(admin.StackedInline):
    model = FileUser
    extra = 1


class UserDataAdmin(admin.ModelAdmin):
    inlines = [
        AdminFileUser,
    ]
    list_display = ('get_avatar_user', 'author_username', 'first_name', 'patronymic', 'last_name',  'email', 'address_ward',
                    'about_me', 'status', 'is_active', )
    list_display_links = ('get_avatar_user', 'author_username')
    list_filter = ('status', 'is_active')
    search_fields = ('first_name', 'author_username')

    def get_avatar_user(self, object):
        if object.avatar_user:
            return mark_safe(f'<img src="{object.avatar_user.url}" width=50>')
    get_avatar_user.short_description = 'Аватар'

    def author_username(self, obj):
        return obj.username
    author_username.short_description = 'Номер телефона'

    def get_fields(self, request, obj=None):
        if obj:
            if obj.status == 'ward':
                return ['username', 'first_name', 'last_name', 'patronymic', 'status', 'is_active', 'phone', 'email',
                  'address_ward', 'about_me', 'avatar_user', ]

            else:
                return ['username', 'first_name', 'last_name', 'patronymic', 'status', 'is_active', 'phone', 'email',
                        'address_ward', 'about_me', 'avatar_user', 'size_donations', ]
        else:
            return super().get_fields(request, obj)

    def __str__(self):
        return "Пользователи"

    def save_form(self, request, form, change):
        instanse = form.save(commit=False)
        if request.POST.get('is_active'):
            _sending_sms(user=instanse, flag=1)
        return instanse


admin.site.register(UserData, UserDataAdmin)
admin.site.register(FileUser, FileUserAdmin)
admin.site.site_title = 'Панель администратора сайта "Скорей Добрей"'
admin.site.site_header = 'Панель администратора сайта "Скорей Добрей"'
admin.site.unregister(Group)
