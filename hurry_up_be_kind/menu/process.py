import openpyxl
from .models import Menu
from .serializers import SerializerMenu


def _massive_save(menu_file):
    book = openpyxl.open(menu_file, read_only=True)
    sheet = book.active
    for row in range(2, sheet.max_row + 1):
        x = {'section_menu': sheet[row][0].value,
             'name_dish': sheet[row][1].value,
             'weight_dish': sheet[row][2].value,
             'price_dish': sheet[row][3].value,
             'description_dish': sheet[row][4].value,
             'composition_dish': sheet[row][5].value
             }
        serializer = SerializerMenu(data=x)
        serializer.is_valid(raise_exception=True)

        Menu.objects.create(
            section_menu=sheet[row][0].value,
            name_dish=sheet[row][1].value,
            weight_dish=sheet[row][2].value,
            price_dish=sheet[row][3].value,
            description_dish=sheet[row][4].value,
            composition_dish=sheet[row][5].value
        )

    return {'content': "Записи успешно добавлены"}