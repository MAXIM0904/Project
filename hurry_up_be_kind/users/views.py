from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from .models import UserData
from .serializers import UserUpdateSerializer, AllUserSerializer
from . import process
from django.shortcuts import redirect


def home_page(request):
    return redirect('/hurry_up_be_kind/index', permanent=True)


class RegistrationUser(APIView):
    """ Класс регистрации пользователя """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            create_user = process._create_user(request=request)
        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})
        return JsonResponse({'registration': 'True',
                             'id': str(create_user.id)}, json_dumps_params={'ensure_ascii': False})


class InfUser(APIView):
    """ Класс возвращает информацию о пользователе """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        context = process._inf_user(request)
        return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


class UpdateUser(APIView):
    """ Класс изменения данных пользователя """
    permission_classes = (IsAuthenticated,)

    def patch(self, request, *args, **kwargs):
        user_form = UserUpdateSerializer(request.user, request.data, partial=True)
        user_form.is_valid(raise_exception=True)
        process._save_data_user(request=request, user_form=user_form)
        context = process._inf_user(request)
        return JsonResponse(context, json_dumps_params={'ensure_ascii': False})


class DeleteUser(APIView):
    """ Класс удаления данный пользователя """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        process._delete_user(request)
        return JsonResponse({'status': True})


class AllUsers(ListAPIView):
    """ Предоставление всех пользователей в базе данных """
    permission_classes = (IsAdminUser,)
    queryset = UserData.objects.all()
    serializer_class = AllUserSerializer


class AllWard(ListAPIView):
    """ Предоставление всех подопечных в базе данных """
    permission_classes = (IsAuthenticated,)
    queryset = UserData.objects.filter(status="ward")
    serializer_class = AllUserSerializer


class AllPhilantropist(ListAPIView):
    """ Предоставление всех филантропов в базе данных """
    permission_classes = (IsAdminUser,)
    queryset = UserData.objects.filter(status="philantropist")
    serializer_class = AllUserSerializer


class VerificationSms(APIView):
    """ Класс верификации пользователя по СМС """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            verification_code = int(request.data['verification_code'])
            user = UserData.objects.get(id=request.data['id'])
            answer = process._verification_user(user=user, verification_code=verification_code)
            return JsonResponse(answer)

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})


class PasswordRecovery(APIView):
    """ Класс восстановления пароля """
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            user = UserData.objects.get(username=request.data['phone'])
            user.random_number = process._random_int()
            user.save()
            process._sending_sms(user=user)
            return JsonResponse({'registration': 'True',
                                 'id': 'Введите пароль из СМС'})

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)})

    def patch(self, request):
        try:
            user = UserData.objects.get(username=request.data['phone'])
            verification_code = int(request.data['verification_code'])
            new_password = request.data['password']
            process._verification_code(user=user, verification_code=verification_code)
            password = make_password(password=new_password, salt=None, hasher='default')
            user.password = password
            user.save()
            answer = process._get_tokens_for_user(user=user)
            return JsonResponse(answer)

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})
