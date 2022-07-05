from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ('get_img_dish', 'name_dish', 'weight_dish', 'price_dish', 'section_menu',
                    'description_dish', 'composition_dish')
    list_display_links = ('get_img_dish', 'name_dish')
    list_filter = ('name_dish', 'composition_dish', 'price_dish')
    search_fields = ('name_dish', 'composition_dish', 'description_dish')


    def get_img_dish(self, object):
        if object.img_dish:
            return mark_safe(f'<img src="{object.img_dish.url}" width=50>')


admin.site.register(Menu, MenuAdmin)
