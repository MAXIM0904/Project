# Generated by Django 4.0.4 on 2022-07-23 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='registrarion_date',
            field=models.DateTimeField(default='2022-07-23 19:50:17', verbose_name='Дата регистрации'),
        ),
    ]
