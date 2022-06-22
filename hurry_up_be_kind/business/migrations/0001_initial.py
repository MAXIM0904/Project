# Generated by Django 4.0.4 on 2022-06-21 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_menu', models.IntegerField(verbose_name='Количество блюд')),
                ('order_status', models.CharField(choices=[('generated', 'generated'), ('paid_for', 'paid_for'), ('admitted', 'admitted'), ('completed', 'completed'), ('archive', 'archive')], max_length=200, verbose_name='Статус заказа')),
                ('price_order', models.IntegerField(default=0, verbose_name='Цена заказа')),
                ('order_date', models.DateTimeField(default='2022-06-21 14:10:08', verbose_name='Дата создания корзины')),
            ],
            options={
                'verbose_name': 'Корзина',
                'verbose_name_plural': 'Содержимое корзины',
                'ordering': ['price_order'],
            },
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField(blank=True, default=0, null=True, verbose_name='Количество заказанного товара')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order', to='business.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_items', to='menu.menu')),
            ],
            options={
                'verbose_name': 'Товары',
                'verbose_name_plural': 'Товары в корзине',
            },
        ),
    ]
