from requests import Response

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import JsonResponse
from .serializers import UserRegistrationSerializer, UserUpdateSerializer
from . import process

class RegistrationUser(APIView):
    """ Класс регистрации пользователя """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            process._create_user(serializer_form=serializer)
        except Exception as error:
            return JsonResponse({'error': str(error)})

        return JsonResponse({'registration': True})


class InfUser(APIView):
    '''Класс возвращает информацию о пользователе'''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = process._inf_user(request)
        return JsonResponse(context)


class UpdateUser(APIView):
    '''Класс изменения данных пользователя'''
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        user_form = UserUpdateSerializer(request.user, request.data, partial=True)
        user_form.is_valid(raise_exception=True)
        process._save_data_user(request=request, user_form=user_form)
        context = process._inf_user(request)
        return JsonResponse(context)


class DeleteUser(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        process._delete_user(request)
        return JsonResponse({'status': True})
