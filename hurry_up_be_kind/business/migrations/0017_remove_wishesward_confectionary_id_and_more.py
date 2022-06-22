# Generated by Django 4.0.4 on 2022-06-22 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('confectionary', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('menu', '0001_initial'),
        ('business', '0016_alter_ordertaken_options_alter_wishesward_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishesward',
            name='confectionary_id',
        ),
        migrations.RemoveField(
            model_name='wishesward',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='wishesward',
            name='ward_id',
        ),
        migrations.AddField(
            model_name='wishesward',
            name='confectionary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='confectionary', to='confectionary.confectionary'),
        ),
        migrations.AddField(
            model_name='wishesward',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='product', to='menu.menu'),
        ),
        migrations.AddField(
            model_name='wishesward',
            name='ward',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ward', to=settings.AUTH_USER_MODEL),
        ),
    ]
