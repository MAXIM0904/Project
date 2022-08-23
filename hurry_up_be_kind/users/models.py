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
        ("philantropist", "благотворитель"),
        ("ward", "подопечный"),
        ("confectioner", "кондитер"),
    ]

    phone_regex = RegexValidator(
        regex=r'^[7]\d{9,12}$',
        message="Номер телефона должен быть введен в формате: '79101111111'. Допускается до 12 цифр."
    )
    phone = models.CharField(('Номер телефона'), validators=[phone_regex], max_length=17)
    patronymic = models.CharField(max_length=150, blank=True, null=True, verbose_name="Отчество")
    status = models.CharField(max_length=14, choices=STATUS_CHOICES, verbose_name="Статус пользователя")
    size_donations = models.IntegerField(default=0, verbose_name="Размер пожертвований")
    address_ward = models.TextField(default="", verbose_name="Адрес места нахождения")
    is_active = models.BooleanField(
        ('Активность'), default=False,
        help_text=('Определяет, следует ли рассматривать этого пользователя как активного. ',
                   "Отмените выбор этого параметра вместо удаления учетных записей.")
    )
    about_me = models.TextField(verbose_name="О себе", blank=True)
    registrarion_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    random_number = models.IntegerField(verbose_name="Код верификации", default=0)
    email = models.EmailField(('E-mail'), blank=True, null=True, default=None)
    avatar_user = models.ImageField(upload_to="avatar_user/", verbose_name="Аватар пользователя", null=True, blank=True)


    class Meta:
        ordering = ["status"]
        verbose_name_plural = 'Пользователи'
        verbose_name = 'пользователя'


    def __str__(self):
        return str(self.username)


class FileUser(models.Model):
    """
    Модель добавления файлов пользователем
    file_user принимает любые файлы
    """
    model_file = models.ForeignKey('UserData', on_delete=models.CASCADE, related_name='model_file')
    file_user = models.FileField(upload_to="file_user/", verbose_name="Файлы пользователя", blank=True)

    class Meta:
        verbose_name_plural = 'Файлы пользователей'
        verbose_name = 'файлы пользователя'


    def __str__(self):
        return str(self.file_user)
