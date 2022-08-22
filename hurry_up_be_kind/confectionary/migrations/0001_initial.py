# Generated by Django 4.0.4 on 2022-08-21 14:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Confectionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confectionary_name', models.CharField(blank=True, max_length=100, verbose_name='Название кондитерской')),
                ('number_phone', models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер телефона кондитерской')),
                ('description_confectionary', models.TextField(blank=True, verbose_name='Описание')),
                ('address_ward', models.TextField(blank=True, verbose_name='Адрес кондитерской')),
                ('avatar_confectionary', models.ImageField(blank=True, null=True, upload_to='avatar_confectionary/', verbose_name='Аватар кондитерской')),
            ],
            options={
                'verbose_name': 'кондитерские',
                'verbose_name_plural': 'Кондитерские',
            },
        ),
        migrations.CreateModel(
            name='ImgFileConfectionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_confectionary', models.ImageField(blank=True, null=True, upload_to='img_confectionary/', verbose_name='Фото кондитерской')),
                ('file_confectionary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='file_confectionary', to='confectionary.confectionary')),
            ],
        ),
    ]
