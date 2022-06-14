# Generated by Django 4.0.4 on 2022-06-10 14:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userdata_patronymic_alter_userdata_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='phone',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '79101111111'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='phone number'),
        ),
    ]
