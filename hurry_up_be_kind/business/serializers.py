from rest_framework import serializers
from .models import Order
from users.models import UserData
from confectionary.models import Confectionary
from menu.models import Menu


class UserPhilantropistSerializer(serializers.ModelSerializer):
    """Сериализация модели пользователя для раскрытия нужных полей вложенного словаря"""
    class Meta:
        model = UserData
        fields = ('id', 'first_name', 'last_name')


class UserConfectionarySerializer(serializers.ModelSerializer):
    """Сериализация модели кондитерской для раскрытия нужных полей вложенного словаря"""
    class Meta:
        model = Confectionary
        fields = ('id', 'confectionary_name', 'address_ward')


class UserProductSerializer(serializers.ModelSerializer):
    """Сериализация модели меню для раскрытия нужных полей вложенного словаря"""
    class Meta:
        model = Menu
        fields = ('id', 'name_dish', 'section_menu', 'price_dish')


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализация корзины """
    user_philantropist_id = UserPhilantropistSerializer(many=False, read_only=True)
    confectionary_id = UserConfectionarySerializer(many=False, read_only=True)
    product_id = UserProductSerializer(many=False, read_only=True)
    user_ward_id = UserPhilantropistSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user_philantropist_id', 'confectionary_id',
                  'user_ward_id', 'product_id', 'count_menu', 'order_status', 'price_order')
