# Generated by Django 4.0.4 on 2022-06-07 19:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '79101111111'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number')),
                ('message_text', models.TextField(verbose_name='Текст сообщения')),
                ('status', models.CharField(choices=[('received', 'received'), ('archive', 'archive')], default='received', max_length=9, verbose_name='Статус сообщения')),
                ('registrarion_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
            ],
            options={
                'ordering': ['status'],
            },
        ),
    ]
