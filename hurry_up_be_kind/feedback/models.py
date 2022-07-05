from django.core.validators import RegexValidator
from django.db import models
from datetime import datetime

class Feedback(models.Model):
    STATUS_CHOICES = [
        ("received", "received"),
        ("archive", "archive"),
    ]

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '79101111111'. Up to 15 digits allowed."
    )
    phone = models.CharField(('phone number'), validators=[phone_regex], max_length=17)
    message_text = models.TextField(verbose_name="Текст сообщения")
    status = models.CharField(max_length=9, choices=STATUS_CHOICES, verbose_name="Статус сообщения", default='received')
    registrarion_date = models.DateTimeField(
        default=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), verbose_name="Дата регистрации"
    )


    class Meta:
        ordering = ["status"]
        verbose_name = 'сообщение обратной связи'
        verbose_name_plural = 'Обратная связь'


    def __str__(self):
        return str(self.id)
