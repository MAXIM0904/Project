from rest_framework import serializers
from .models import Order, OrderExecution


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализация корзины """

    class Meta:
        model = Order
        fields = ('id', 'user_philantropist_id', 'confectionary_id',
                  'user_ward_id', 'product_id', 'count_menu', 'order_status', 'price_order')


class OrderExecutionSerializer(serializers.ModelSerializer):
    """ Сериализация корзины """

    class Meta:
        model = OrderExecution
        fields = ('id', 'order_execution', 'order_status_execution')
