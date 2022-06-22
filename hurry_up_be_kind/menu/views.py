from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from .models import Menu
from django.http import JsonResponse
from .serializers import SerializerMenu
from .forms import MassiveMenuUpdateForm
from . import process


class RegisterMenu(CreateAPIView):
    """ Рeгистрация отдельного меню """
    permission_classes = (IsAdminUser,)
    serializer_class = SerializerMenu

    def get(self, request):
        types_menu = dict(Menu.SECTION)
        return JsonResponse(types_menu)


class AllEconomyMenu(ListAPIView):
    """ Все позиции экономного меню """
    permission_classes = (IsAdminUser,)
    queryset = Menu.objects.filter(section_menu='эконом')
    serializer_class = SerializerMenu


class AllOptimalMenu(ListAPIView):
    """ Все позиции оптимального меню """
    permission_classes = (IsAdminUser,)
    queryset = Menu.objects.filter(section_menu='оптимальный')
    serializer_class = SerializerMenu


class AllBusinessMenu(ListAPIView):
    """ Все позиции бизнес меню """
    permission_classes = (IsAdminUser,)
    queryset = Menu.objects.filter(section_menu='бизнес')
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
                return JsonResponse(result)
            else:
                raise ValueError(update_menu.errors.as_data())

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)})
