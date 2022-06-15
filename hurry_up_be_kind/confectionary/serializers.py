from rest_framework import serializers
from .models import Confectionary


class ConfectionarySerializer(serializers.ModelSerializer):
    ''' Сериализация данных кондитерской '''

    img_confectionary = serializers.ImageField()

    class Meta:
        model = Confectionary
        fields = ('confectionary_name', 'number_phone', 'description_confectionary',
                  'address_ward', 'img_confectionary')

class ConfectionaryAllSerializer(serializers.ModelSerializer):
    ''' Сериализация данных кондитерской '''

    class Meta:
        model = Confectionary
        fields = ('id', 'confectionary_name', 'number_phone', 'description_confectionary',
                  'address_ward')