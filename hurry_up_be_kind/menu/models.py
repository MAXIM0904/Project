from django.db import models


class Menu(models.Model):
    ''' Модель блюд, которых предлагает кондитерская '''
    SECTION = [
        ("economy", "эконом"),
        ("optimal", "оптимальный"),
        ("business", "бизнес"),
    ]
    section_menu = models.CharField(max_length=14, choices=SECTION, verbose_name="Раздел меню")
    name_dish = models.CharField(max_length=255, verbose_name="Название блюда")
    weight_dish = models.CharField(max_length=50, verbose_name="Вес блюда")
    price_dish = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Цена блюда")
    description_dish = models.TextField(verbose_name="Описание")
    composition_dish = models.TextField(verbose_name="Состав блюда")
    img_dish = models.ImageField(upload_to="img_dish/", verbose_name="Фото блюда", null=True, blank=True)


    class Meta:
        ordering = ["price_dish"]
        verbose_name = 'пункты меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name_dish
