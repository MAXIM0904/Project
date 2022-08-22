# from datetime import datetime
from django.db import models
from users.models import UserData
from menu.models import Menu
from confectionary.models import Confectionary

STATUS_ORDER = [
    ("generated", "создан"),
    ("paid_for", "оплачен"),
    ("formed", "сформирован"),
    ("desire_ward", "желание подопечного"),
    ("admitted", "принят"),
    ("completed", "выполнен"),
    ("archive", "архивный"),
]

class Order(models.Model):
    """ Модель корзины пользователя """
    user_philantropist_id = models.ForeignKey(UserData, on_delete=models.SET_NULL, null=True, related_name="user_philantropist")
    confectionary_id = models.ForeignKey(Confectionary, on_delete=models.SET_NULL, null=True, related_name="user_confectioner")
    user_ward_id = models.ForeignKey(UserData, on_delete=models.SET_NULL, null=True, related_name="user_ward")
    product_id = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, related_name='order_items')
    count_menu = models.IntegerField(verbose_name="Количество блюд", default=1)
    order_status = models.CharField(max_length=200, choices=STATUS_ORDER, default='generated', verbose_name="Статус заказа")
    price_order = models.IntegerField(verbose_name="Цена заказа", default=0)
    # order_date = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name="Дата создания корзины")

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Содержимое корзины'

    def __str__(self):
        return str(self.count_menu)


class OrderExecution(models.Model):
    order_execution = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_execution")
    order_status_execution = models.CharField(max_length=200, choices=STATUS_ORDER, default='paid_for', verbose_name="Статус заказа")
