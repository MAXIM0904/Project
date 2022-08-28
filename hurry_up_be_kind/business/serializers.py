from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализация корзины """

    class Meta:
        model = Order
        fields = ('id', 'user_philantropist_id', 'confectionary_id',
                  'user_ward_id', 'product_id', 'count_menu', 'order_status', 'price_order')
