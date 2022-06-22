# from datetime import datetime
from django.db import models
from users.models import UserData
from menu.models import Menu
from confectionary.models import Confectionary


class Order(models.Model):
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
    user_philantropist_id = models.ForeignKey(UserData, on_delete=models.SET_NULL, null=True, related_name="user_philantropist")
    confectionary_id = models.ForeignKey(Confectionary, on_delete=models.SET_NULL, null=True, related_name="user_confectioner")
    user_ward_id = models.ForeignKey(UserData, on_delete=models.SET_NULL, null=True, related_name="user_ward")
    product_id = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, related_name='order_items')
    count_menu = models.IntegerField(verbose_name="Количество блюд")
    order_status = models.CharField(max_length=200, choices=STATUS_ORDER, default='generated', verbose_name="Статус заказа")
    price_order = models.IntegerField(verbose_name="Цена заказа", default=0)
    # order_date = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name="Дата создания корзины")

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Содержимое корзины'


    def __str__(self):
        return str(self.count_menu)


class WishesWard(models.Model):

    STATUS_ORDER = [
        ("generated", "generated"), #создан
        ("paid_for", "paid_for"), #оплачен
        ("admitted", "admitted"), #принят
        ("completed", "completed"), #выполнен
        ("archive", "archive"), #архивный
        ]

    ward = models.ForeignKey(UserData, on_delete=models.SET_NULL, null=True, related_name="ward")
    product = models.ForeignKey(Menu, on_delete=models.SET_NULL, null=True, related_name='product')
    confectionary = models.ForeignKey(Confectionary, on_delete=models.SET_NULL, null=True, related_name="confectionary")
    count_product = models.IntegerField(verbose_name="Количество блюд")
    order_status = models.CharField(max_length=200, choices=STATUS_ORDER, default='generated',
                                    verbose_name="Статус заказа")

    class Meta:
        verbose_name = 'Желания'
        verbose_name_plural = 'Желание подопечного'


    def __str__(self):
        return str(self.ward)


class OrderTaken(models.Model):
    user_philantropist_id = models.ForeignKey(UserData, on_delete=models.SET_NULL, null=True,
                                              related_name="user_philantropist_id")
    wishes_ward_id = models.ForeignKey(WishesWard, on_delete=models.SET_NULL, null=True, related_name="wishes_ward_id")


    class Meta:
        verbose_name = 'Взятые заказы'
        verbose_name_plural = 'Взятые заказы'


    def __str__(self):
        return str(self.user_philantropist_id)
