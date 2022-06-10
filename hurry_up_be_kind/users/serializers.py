from rest_framework import serializers
from .models import UserData


class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' Сериализатор регистрации нового пользователя '''

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'phone', 'status', 'password', 'random_number', 'patronymic')


class UserUpdateSerializer(serializers.ModelSerializer):
    ''' Сериализация изменения данных профиля UserData '''

    image = serializers.ImageField()

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'patronymic', 'phone', 'address_ward', 'about_me', 'image')


class AllUserSerializer(serializers.ModelSerializer):
    ''' Сериализация данных профиля '''

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'patronymic', 'phone', 'address_ward', 'about_me',
                  'status', 'size_donations')

