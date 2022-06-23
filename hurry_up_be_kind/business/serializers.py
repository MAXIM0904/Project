from rest_framework import serializers
from .models import Order, WishesWard, OrderTaken


# class OrderSerializer(serializers.ModelSerializer):
#     ''' Сериализация данных кондитерской '''
#
#     class Meta:
#         model = Order
#         fields = ('user_philantropist_id', 'confectionary_id', 'user_ward_id', 'product_id', 'count_menu',
#                   'price_order')

class WishesWardSerializer(serializers.ModelSerializer):
    ''' Сериализация желания подопечного '''

    class Meta:
        model = WishesWard
        fields = ('product', 'count_product', 'ward', 'confectionary', 'order_wishes')


class InfoWishesWardSerializer(serializers.ModelSerializer):
    ''' Сериализация информации о желаниях подопечного '''

    class Meta:
        model = WishesWard
        fields = ('id', 'ward', 'product', 'confectionary', 'count_product', 'order_wishes')



class OrderTakenSerializer(serializers.ModelSerializer):
    ''' Сериализация информации о взятых заказах '''

    class Meta:
        model = OrderTaken
        fields = ('id', 'user_philantropist_id', 'wishes_ward_id', 'order_status')


class MakeGiftSerializer(serializers.ModelSerializer):
    ''' Сериализация модели - сделать подарок '''

    class Meta:
        model = Order
        fields = ('id', 'user_philantropist_id', 'confectionary_id',
                  'user_ward_id','product_id', 'count_menu', 'order_status')