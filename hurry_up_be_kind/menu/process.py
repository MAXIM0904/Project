import openpyxl
from .models import Menu
from .serializers import SerializerMenu


def _massive_save(menu_file):
    book = openpyxl.open(menu_file, read_only=True)
    sheet = book.active
    for row in range(2, sheet.max_row + 1):
        dict_menu = {'section_menu': sheet[row][0].value,
             'name_dish': sheet[row][1].value,
             'weight_dish': sheet[row][2].value,
             'price_dish': sheet[row][3].value,
             'description_dish': sheet[row][4].value,
             'composition_dish': sheet[row][5].value
             }
        serializer = SerializerMenu(data=dict_menu)
        serializer.is_valid(raise_exception=True)
        instance = Menu(
            section_menu=sheet[row][0].value,
            name_dish=sheet[row][1].value,
            weight_dish=sheet[row][2].value,
            price_dish=sheet[row][3].value,
            description_dish=sheet[row][4].value,
            composition_dish=sheet[row][5].value
        )
        instance_menu = Menu.objects.filter(name_dish=instance.name_dish, section_menu=instance.section_menu)
        if instance_menu:
            instance_menu[0].weight_dish = instance.weight_dish
            instance_menu[0].price_dish = instance.price_dish
            instance_menu[0].description_dish = instance.description_dish
            instance_menu[0].composition_dish = instance.composition_dish
            instance_menu[0].save()
        else:
            instance.save()
    return "Записи успешно добавлены"