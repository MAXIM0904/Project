# Generated by Django 4.0.4 on 2022-06-23 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0018_remove_wishesward_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishesward',
            name='count_product',
            field=models.IntegerField(default=1, verbose_name='Количество блюд'),
        ),
    ]
