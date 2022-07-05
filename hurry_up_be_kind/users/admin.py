from django.contrib import admin
from django.utils.safestring import mark_safe
from django.contrib.auth.models import Group
from .process import _sending_sms


from .models import UserData, AvatarUser



class AvatarUserAdmin(admin.ModelAdmin):
    list_display = ('model_file', 'file_user', )
    search_fields = ('file_user',)


class AdminAvatarUser(admin.StackedInline):
    model = AvatarUser
    extra = 1


class UserDataAdmin(admin.ModelAdmin):
    inlines = [
        AdminAvatarUser,
    ]
    list_display = ('get_avatar_user', 'username', 'first_name', 'last_name', 'patronymic', 'email', 'address_ward',
                    'about_me', 'status', 'is_active', )
    list_display_links = ('get_avatar_user', 'username')
    list_filter = ('status', 'is_active')
    search_fields = ('first_name', 'username')


    def get_avatar_user(self, object):
        if object.avatar_user:
            return mark_safe(f'<img src="{object.avatar_user.url}" width=50>')


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
        print(request.POST['username'])
        instanse = form.save(commit=False)
        if request.POST.get('is_active'):
            _sending_sms(user=instanse, flag=1)
            print('po[op')
        return instanse


admin.site.register(UserData, UserDataAdmin)
admin.site.register(AvatarUser, AvatarUserAdmin)
admin.site.site_title = 'Панель администратора сайта "Скорей Добрей"'
admin.site.site_header = 'Панель администратора сайта "Скорей Добрей"'
admin.site.unregister(Group)
