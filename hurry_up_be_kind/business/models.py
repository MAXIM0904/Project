from django.db import models
from users.models import UserData
from confectionary.models import Menu

class Basket(models.Model):
    '''
    Модель корзины пользователя
    '''

    STATUS_ORDER = [
        ("generated", "generated"), #создан
        ("paid_for", "paid_for"), #оплачен
        ("admitted", "admitted"), #принят
        ("completed", "completed"), #выполнен
        ("archive", "archive"), #архивный
    ]

    user_philantropist = models.ManyToManyField(UserData, blank=True, related_name="user_philantropist")
    user_ward = models.ManyToManyField(UserData, blank=True, related_name="user_ward")
    user_confectionary = models.ManyToManyField(Menu, related_name="user_confectionary")

    count_menu = models.IntegerField(verbose_name="Количество блюд")
    order_status = models.CharField(max_length=200, choices=STATUS_ORDER, verbose_name="Статус заказа")
    price_order = models.IntegerField(verbose_name="Цена заказа", default=0)

    def __str__(self):
        return self.order_status
