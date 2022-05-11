from django.contrib import admin
from .models import Confectionary, Menu, ImgFileConfectionary, ImgFileMenu

class ImgFileConfectionaryAdmin(admin.ModelAdmin):
    pass


class ImgFileMenuAdmin(admin.ModelAdmin):
    pass


class AdminImgFileConfectionary(admin.TabularInline):
    model = ImgFileConfectionary


class ConfectionaryAdmin(admin.ModelAdmin):
    inlines = [
        AdminImgFileConfectionary,
    ]


class AdminImgFileMenu(admin.TabularInline):
    model = ImgFileMenu


class MenuAdmin(admin.ModelAdmin):
    inlines = [
        AdminImgFileMenu,
    ]

admin.site.register(Confectionary, ConfectionaryAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(ImgFileMenu, ImgFileMenuAdmin)
admin.site.register(ImgFileConfectionary, ImgFileConfectionaryAdmin)
