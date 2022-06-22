# Generated by Django 4.0.4 on 2022-06-21 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section_menu', models.CharField(choices=[('эконом', 'эконом'), ('оптимальный', 'оптимальный'), ('бизнес', 'бизнес')], max_length=14, verbose_name='Раздел меню')),
                ('name_dish', models.CharField(max_length=200, verbose_name='Название блюда')),
                ('weight_dish', models.CharField(max_length=50, verbose_name='Вес блюда')),
                ('price_dish', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Цена блюда')),
                ('description_dish', models.TextField(max_length=255, verbose_name='Описание')),
                ('composition_dish', models.TextField(max_length=255, verbose_name='Состав блюда')),
                ('img_dish', models.ImageField(blank=True, null=True, upload_to='img_dish/', verbose_name='Фото блюда')),
            ],
            options={
                'verbose_name': 'Меню',
                'verbose_name_plural': 'Пункты меню',
                'ordering': ['price_dish'],
            },
        ),
    ]
