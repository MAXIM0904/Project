from rest_framework import serializers
from .models import UserData


class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' Сериализатор регистрации нового пользователя '''

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'phone', 'password', 'status')


class UserUpdateSerializer(serializers.ModelSerializer):
    ''' Сериализация изменения данных профиля User '''

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'phone', 'address_ward', 'about_me',)
