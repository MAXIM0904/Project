from django.db import models
from django.contrib.auth.models import AbstractUser

class UserData(AbstractUser):
    STATUS_CHOICES = [
        ("p", "Philantropist"),
        ("w", "Ward"),
        ('c', 'Confectionary'),
    ]
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="Статус пользователя")
    size_donations = models.IntegerField(default=0, verbose_name='Размер пожертвований')
    address_ward = models.TextField(default='', verbose_name='Адрес места нахождения')
    about_me = models.TextField(verbose_name="О себе", blank=True)
    registrarion_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    avatar_user_img = models.ImageField(
        upload_to='avatar_philantropist/', verbose_name='Аватар профиля', null=True, blank=True
    )

    class Meta:
        ordering = ["status"]

    def __str__(self):
        return str(self.username)


class Menu(models.Model):
    name_confectionary = models.ForeignKey(
        "UserData", null=True, default="", on_delete=models.CASCADE, related_name='menu_confectionary'
    )
    name_dish = models.CharField(max_length=200, verbose_name="Название блюда")
    price_dish = models.IntegerField(verbose_name="Название блюда")
    text_comment = models.TextField(verbose_name="Комментарий к блюду")
    img_dish = models.ImageField(upload_to='img_dish/', verbose_name='Фото блюда', null=True, blank=True)

    class Meta:
        ordering = ["price_dish"]

    def __str__(self):
        return self.name_dish