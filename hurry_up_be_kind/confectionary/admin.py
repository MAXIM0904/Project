from django.contrib import admin
from .models import Confectionary


class ConfectionaryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Confectionary, ConfectionaryAdmin)
