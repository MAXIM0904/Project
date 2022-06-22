from django.contrib import admin
from .models import Order, WishesWard, OrderTaken


class OrderAdmin(admin.ModelAdmin):
    pass


class WishesWardAdmin(admin.ModelAdmin):
    pass


class OrderTakenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Order, OrderAdmin)
admin.site.register(WishesWard, WishesWardAdmin)
admin.site.register(OrderTaken, OrderTakenAdmin)
