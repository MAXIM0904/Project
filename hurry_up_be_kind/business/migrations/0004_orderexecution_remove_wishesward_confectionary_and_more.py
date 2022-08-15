# Generated by Django 4.0.4 on 2022-08-15 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderExecution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_status', models.CharField(choices=[('generated', 'создан'), ('paid_for', 'оплачен'), ('formed', 'сформирован'), ('desire_ward', 'желание подопечного'), ('admitted', 'принят'), ('completed', 'выполнен'), ('archive', 'архивный')], default='generated', max_length=200, verbose_name='Статус заказа')),
            ],
        ),
        migrations.RemoveField(
            model_name='wishesward',
            name='confectionary',
        ),
        migrations.RemoveField(
            model_name='wishesward',
            name='product',
        ),
        migrations.RemoveField(
            model_name='wishesward',
            name='ward',
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('generated', 'создан'), ('paid_for', 'оплачен'), ('formed', 'сформирован'), ('desire_ward', 'желание подопечного'), ('admitted', 'принят'), ('completed', 'выполнен'), ('archive', 'архивный')], default='generated', max_length=200, verbose_name='Статус заказа'),
        ),
        migrations.DeleteModel(
            name='OrderTaken',
        ),
        migrations.DeleteModel(
            name='WishesWard',
        ),
        migrations.AddField(
            model_name='orderexecution',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_execution', to='business.order'),
        ),
    ]
