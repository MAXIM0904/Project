# Generated by Django 4.0.4 on 2022-06-21 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_rename_user_confectioner_order_confectionary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_date',
        ),
    ]