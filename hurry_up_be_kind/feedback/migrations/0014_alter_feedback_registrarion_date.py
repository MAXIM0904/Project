# Generated by Django 4.0.4 on 2022-06-22 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0013_alter_feedback_registrarion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='registrarion_date',
            field=models.DateTimeField(default='2022-06-22 14:05:03', verbose_name='Дата регистрации'),
        ),
    ]
