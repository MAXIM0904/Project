# Generated by Django 4.0.4 on 2022-06-21 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0007_alter_feedback_registrarion_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='registrarion_date',
            field=models.DateTimeField(default='2022-06-21 14:30:06', verbose_name='Дата регистрации'),
        ),
    ]
