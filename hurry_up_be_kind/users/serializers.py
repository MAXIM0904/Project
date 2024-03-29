from rest_framework import serializers
from .models import UserData


class UserRegistrationSerializer(serializers.ModelSerializer):
    ''' Сериализатор регистрации нового пользователя '''
    save_file = serializers.FileField(required=False)

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'patronymic', 'phone', 'email', 'status', 'password',
                  'random_number', 'save_file',)


class UserUpdateSerializer(serializers.ModelSerializer):
    ''' Сериализация изменения данных профиля UserData '''

    save_file = serializers.FileField()

    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'patronymic', 'phone', 'email', 'address_ward',
                  'about_me', 'save_file', 'avatar_user')


class AllUserSerializer(serializers.ModelSerializer):
    ''' Сериализация данных профиля '''

    class Meta:
        model = UserData
        fields = ('id', 'first_name', 'last_name', 'patronymic', 'phone', 'email', 'address_ward', 'about_me',
                  'status', 'size_donations', 'avatar_user')
