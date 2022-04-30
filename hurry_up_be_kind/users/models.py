from django.db import models
from django.contrib.auth.models import AbstractUser


class UserData(AbstractUser):
    """
    Модель пользователя. Разрешает регистрироваться:
    1. philantropist - благотворитель,
    2. ward - подопечный,
    3. confectioner - руководитель кондитерской (сети кондитерских).
    """

    STATUS_CHOICES = [
        ("philantropist", "philantropist"),
        ("ward", "ward"),
        ("confectioner", "confectioner"),
    ]
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, verbose_name="Статус пользователя")
    size_donations = models.IntegerField(default=0, verbose_name="Размер пожертвований")

    address_ward = models.TextField(default="", verbose_name="Адрес места нахождения")

    about_me = models.TextField(verbose_name="О себе", blank=True)
    registrarion_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    link_user_img = models.URLField(max_length=200, verbose_name="Ссылка на аватарку профиля", blank=True)


    class Meta:
        ordering = ["status"]

    def __str__(self):
        return str(self.username)


class AvatarUser(models.Model):
    """
    Модель добавления аватара пользователя
    avatar_user_img принимает Images
    """
    model_file = models.OneToOneField('UserData', on_delete=models.CASCADE)
    avatar_user_img = models.ImageField(upload_to="avatar_philantropist/", verbose_name="Аватар профиля", blank=True)
