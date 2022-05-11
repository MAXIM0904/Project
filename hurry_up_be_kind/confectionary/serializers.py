from rest_framework import serializers
from .models import Confectionary


class ConfectionarySerializer(serializers.ModelSerializer):
    ''' Сериализация данных кондитерской '''

    img_confectionary = serializers.ImageField()

    class Meta:
        model = Confectionary
        fields = ('director', 'password', 'confectionary_name', 'number_phone',
                  'description_confectionary', 'address_ward', 'img_confectionary')
