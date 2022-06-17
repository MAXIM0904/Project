from _csv import reader
from django.shortcuts import render
from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Menu
from django.http import JsonResponse
from .serializers import SerializerMenu
from .forms import MassiveMenuUpdateForm
import openpyxl


class RegisterMenu(CreateAPIView):
    """ Рeгистрация отдельного меню """
    permission_classes = (AllowAny,)
    serializer_class = SerializerMenu

    def get(self, request):
        types_menu = dict(Menu.SECTION)
        return JsonResponse(types_menu)


class AllEconomyMenu(ListAPIView):
    """ Все позиции экономного меню """
    permission_classes = (AllowAny,)
    queryset = Menu.objects.filter(section_menu='эконом')
    serializer_class = SerializerMenu


class AllOptimalMenu(ListAPIView):
    """ Все позиции экономного меню """
    permission_classes = (AllowAny,)
    queryset = Menu.objects.filter(section_menu='оптимальный')
    serializer_class = SerializerMenu


class AllBusinessMenu(ListAPIView):
    """ Все позиции экономного меню """
    permission_classes = (AllowAny,)
    queryset = Menu.objects.filter(section_menu='бизнес')
    serializer_class = SerializerMenu


class MassiveMenuUpdate(APIView):
    ''' Класс позволяет массово добавлять записи в блог. Использует формат .csv '''
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            update_menu = MassiveMenuUpdateForm(request.POST, request.FILES)
            if update_menu.is_valid():
                menu_file = update_menu.cleaned_data['menu_file']
                book = openpyxl.open(menu_file, read_only=True)
                sheet = book.active
                for row in range(2, sheet.max_row + 1):
                    x = {'section_menu': sheet[row][0].value,
                        'name_dish': sheet[row][1].value,
                        'weight_dish': sheet[row][2].value,
                        'price_dish' : sheet[row][3].value,
                        'description_dish':sheet[row][4].value,
                        'composition_dish': sheet[row][5].value
                         }
                    serializer = SerializerMenu(data=x)
                    serializer.is_valid(raise_exception=True)

                    Menu.objects.create(
                        section_menu=sheet[row][0].value,
                        name_dish=sheet[row][1].value,
                        weight_dish=sheet[row][2].value,
                        price_dish = sheet[row][3].value,
                        description_dish=sheet[row][4].value,
                        composition_dish=sheet[row][5].value
                    )
                return JsonResponse({'content': "Записи успешно добавлены"})

            else:
                raise ValueError(update_menu.errors.as_data())

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)})
