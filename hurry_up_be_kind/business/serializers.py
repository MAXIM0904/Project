from rest_framework import serializers
from .models import Order, WishesWard


# class OrderSerializer(serializers.ModelSerializer):
#     ''' Сериализация данных кондитерской '''
#
#     class Meta:
#         model = Order
#         fields = ('user_philantropist_id', 'confectionary_id', 'user_ward_id', 'product_id', 'count_menu',
#                   'price_order', 'order_status')

class WishesWardSerializer(serializers.ModelSerializer):
    ''' Сериализация желания подопечного '''

    class Meta:
        model = WishesWard
        fields = ('product', 'count_product', 'ward', 'confectionary')


class InfoWishesWardSerializer(serializers.ModelSerializer):
    ''' Сериализация информации о желаниях подопечного '''

    class Meta:
        model = WishesWard
        fields = ('id', 'ward', 'product', 'confectionary', 'count_product', 'order_status')