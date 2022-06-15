from django.db import models
from users.models import UserData


class Confectionary(models.Model):
    ''' Модель кондитерской '''
    director = models.OneToOneField(UserData, on_delete=models.CASCADE, blank=True, related_name="confectionary")
    confectionary_name = models.CharField(max_length=100, verbose_name="Название кондитерской", blank=True)
    number_phone = models.CharField(max_length=100, verbose_name="Номер телефона кондитерской", null=True, blank=True)
    description_confectionary = models.TextField(verbose_name="Описание", blank=True)
    address_ward = models.TextField(verbose_name="Адрес кондитерской", blank=True)


    def __str__(self):
        return self.confectionary_name


class Menu(models.Model):
    ''' Модель блюд, которых предлагает кондитерская '''
    name_confectionary = models.ForeignKey(
        "Confectionary", blank=True, on_delete=models.CASCADE, related_name="menu_confectionary"
    )
    name_dish = models.CharField(max_length=200, verbose_name="Название блюда")
    price_dish = models.IntegerField(verbose_name="Цена блюда")
    description_dish = models.CharField(max_length=500, verbose_name="Описание")


    class Meta:
        ordering = ["price_dish"]

    def __str__(self):
        return self.name_dish


class ImgFileMenu(models.Model):
    '''
    Модель добавления фотографий блюд
    img_dish принимает Images
    '''
    file_menu = models.ForeignKey('Menu', on_delete=models.CASCADE, related_name="file_menu")
    img_dish = models.ImageField(upload_to="img_dish/", verbose_name="Фото блюда", null=True, blank=True)


class ImgFileConfectionary(models.Model):
    '''
    Модель добавления фотографий кондитерской
    file_confectionary принимает Images
    '''
    file_confectionary = models.ForeignKey('Confectionary', on_delete=models.CASCADE, related_name="file_confectionary")
    img_confectionary = models.ImageField(
        upload_to="img_confectionary/", verbose_name="Фото кондитерской", null=True, blank=True
    )
    def __str__(self):
        return str(self.img_confectionary)
