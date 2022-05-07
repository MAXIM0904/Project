# Generated by Django 4.0.4 on 2022-05-06 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_menu', models.IntegerField(verbose_name='Количество блюд')),
                ('order_status', models.CharField(choices=[('generated', 'generated'), ('paid_for', 'paid_for'), ('admitted', 'admitted'), ('completed', 'completed'), ('archive', 'archive')], max_length=200, verbose_name='Статус заказа')),
                ('price_order', models.IntegerField(default=0, verbose_name='Цена заказа')),
            ],
        ),
    ]
