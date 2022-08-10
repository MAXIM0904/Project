from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Confectionary
from . import process
from .serializers import ConfectionarySerializer, ConfectionaryAllSerializer


class RegisterConfectionary(APIView):
    """Класс регистрации кондитерской"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        try:
            if request.user.status == "confectioner":
                user_form = ConfectionarySerializer(request.user, request.data, partial=True)
                user_form.is_valid(raise_exception=True)
                user_form = process._confectionary_save(request=request, confectionary_data=user_form.validated_data)
                inf_confectionary = ConfectionaryAllSerializer(user_form)
                return JsonResponse(inf_confectionary.data)
            else:
                raise ValueError("У вас нет прав на регистрацию кондитерской")

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})


class AllConfectionary(ListAPIView):
    '''Предоставление всех кондитерских в базе данных '''
    permission_classes = (IsAuthenticated,)
    queryset = Confectionary.objects.all()
    serializer_class = ConfectionaryAllSerializer


class UpdateConfectionary(APIView):
    '''Класс изменения данных кондитерской'''
    permission_classes = (IsAuthenticated,)
    serializer_class = ConfectionarySerializer

    def post(self, request, *args, **kwargs):
        instance = request.user.confectionary

        if request.user == instance.director or request.user.is_staff:
            serializer = self.serializer_class(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if process._update_img(request=request, instance=instance, user_form=serializer):
                serializer.save()
            serializer = process._inf_confectionary(instance=instance)
            return JsonResponse(serializer)

        else:
            return JsonResponse(
                {'error': 'Доступ запрещен. Обратитесь к администратору.'},
                json_dumps_params={'ensure_ascii': False}
            )


class DeleteConfectionary(APIView):
    '''Класс удаления кондитерской'''
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            instance = request.user.confectionary
            if request.user == instance.director or request.user.is_staff:
                process._delete_confectionary(request=request)
                return JsonResponse({'status': 'True'})
            else:
                return JsonResponse(
                    {'error': 'Доступ запрещен. Обратитесь к администратору.'},
                    json_dumps_params={'ensure_ascii': False}
                )

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})

class InfConfectionary(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            instance = request.user.confectionary
            inf_confectionary = process._inf_confectionary(instance=instance)
            return JsonResponse(inf_confectionary, json_dumps_params={'ensure_ascii': False})

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})
