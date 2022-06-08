from django.shortcuts import render
from requests import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.http import JsonResponse
from .models import UserData
from .serializers import UserRegistrationSerializer, UserUpdateSerializer, AllUserSerializer
from . import process


def home_page(request):
    return render (request, 'templates/homepage.html', {})


class RegistrationUser(APIView):
    """ Класс регистрации пользователя """
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            create_user = process._create_user(serializer_form=serializer)

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)})

        return JsonResponse({'registration': 'True',
                             'id': str(create_user.id)})


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


class AllUsers(ListAPIView):
    '''Предоставление всех пользователей в базе данных '''
    permission_classes = (IsAdminUser,)
    queryset = UserData.objects.all()
    serializer_class = AllUserSerializer


class AllWard(ListAPIView):
    '''Предоставление всех подопечных в базе данных '''
    permission_classes = (IsAuthenticated,)
    queryset = UserData.objects.filter(status="ward")
    serializer_class = AllUserSerializer


class AllPhilantropist(ListAPIView):
    '''Предоставление всех филантропов в базе данных '''
    permission_classes = (IsAdminUser,)
    queryset = UserData.objects.filter(status="philantropist")
    serializer_class = AllUserSerializer


class Verification_sms(APIView):
    ''' Класс верификации пользователя по СМС '''
    permission_classes = (AllowAny,)

    def post(self, request):
        verification_code = int(request.data['verification_code'])
        user = UserData.objects.get(id=request.data['id'])
        answer = process._verification_user(user=user, verification_code=verification_code)
        return JsonResponse(answer)
