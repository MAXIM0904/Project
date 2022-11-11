from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from .models import Menu
from django.http import JsonResponse
from .serializers import SerializerMenu
from .forms import MassiveMenuUpdateForm
from . import process


class RegisterMenu(CreateAPIView):
    """ Регистрация отдельного меню """
    permission_classes = (IsAdminUser,)
    serializer_class = SerializerMenu

    def get(self, request):
        types_menu = dict(Menu.SECTION)
        return JsonResponse(types_menu, json_dumps_params={'ensure_ascii': False})


class AllEconomyMenu(ListAPIView):
    """ Все позиции экономного меню """
    permission_classes = (IsAuthenticated,)
    queryset = Menu.objects.filter(section_menu='economy')
    serializer_class = SerializerMenu


class AllOptimalMenu(ListAPIView):
    """ Все позиции оптимального меню """
    permission_classes = (IsAuthenticated,)
    queryset = Menu.objects.filter(section_menu='optimal')
    serializer_class = SerializerMenu


class AllBusinessMenu(ListAPIView):
    """ Все позиции бизнес меню """
    permission_classes = (IsAuthenticated,)
    queryset = Menu.objects.filter(section_menu='business')
    serializer_class = SerializerMenu


class MassiveMenuUpdate(APIView):
    ''' Класс позволяет массово добавлять записи в меню. Использует формат .xlsx (Exel) '''
    permission_classes = (IsAdminUser,)

    def post(self, request):
        try:
            update_menu = MassiveMenuUpdateForm(request.POST, request.FILES)
            if update_menu.is_valid():
                menu_file = update_menu.cleaned_data['menu_file']
                result = process._massive_save(menu_file=menu_file)
                return JsonResponse({'registration': 'True',
                                     'id': str(result)}, json_dumps_params={'ensure_ascii': False})
            else:
                raise ValueError(update_menu.errors.as_data())

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)}, json_dumps_params={'ensure_ascii': False})
