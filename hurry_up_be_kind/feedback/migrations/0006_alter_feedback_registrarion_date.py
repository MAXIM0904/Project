# Generated by Django 4.0.4 on 2022-08-06 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_alter_feedback_registrarion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='registrarion_date',
            field=models.DateTimeField(default='2022-08-06 14:32:09', verbose_name='Дата регистрации'),
        ),
    ]
