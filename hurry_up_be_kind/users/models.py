from django.core.validators import RegexValidator
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
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '79101111111'. Up to 15 digits allowed."
    )
    phone = models.CharField(('phone number'), validators=[phone_regex], max_length=17)
    patronymic = models.CharField(max_length=150, blank=True, verbose_name="Отчество")
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, verbose_name="Статус пользователя")
    size_donations = models.IntegerField(default=0, verbose_name="Размер пожертвований")
    address_ward = models.TextField(default="", verbose_name="Адрес места нахождения")
    is_active = models.BooleanField(
        ('active'), default=False,
        help_text=('Designates whether this user should be treated as active. '
                   'Unselect this instead of deleting accounts.')
    )
    about_me = models.TextField(verbose_name="О себе", blank=True)
    registrarion_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    random_number = models.IntegerField(verbose_name="Код верификации", default=0)



    class Meta:
        ordering = ["status"]

    def __str__(self):
        return str(self.username)


class AvatarUser(models.Model):
    """
    Модель добавления аватара пользователя
    avatar_user_img принимает Images
    """
    model_file = models.ForeignKey('UserData', on_delete=models.CASCADE, related_name='model_file')
    avatar_user_img = models.ImageField(upload_to="avatar_philantropist/", verbose_name="Аватар профиля", blank=True)

    def __str__(self):
        return str(self.avatar_user_img)
