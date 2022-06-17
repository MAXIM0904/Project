from rest_framework import serializers
from .models import Menu


class SerializerMenu(serializers.ModelSerializer):
    ''' Сериализатор регистрации меню '''

    class Meta:
        model = Menu
        fields = ('id', 'section_menu', 'name_dish', 'weight_dish', 'price_dish', 'description_dish',
                  'composition_dish', 'img_dish')
