from rest_framework import serializers
from .models import UserData


class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' Сериализатор регистрации нового пользователя '''


    class Meta:
        model = UserData
        fields = ('username', 'first_name', 'last_name', 'phone', 'password', 'status')

    def post_username(self, obj):
        username = obj.phone
        return username


class UserUpdateSerializer(serializers.ModelSerializer):
    ''' Сериализация изменения данных профиля UserData '''

    image = serializers.ImageField()

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'phone', 'address_ward', 'about_me', 'image')

