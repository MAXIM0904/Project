# Generated by Django 4.0.4 on 2022-07-06 08:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('confectionary', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='confectionary',
            name='director',
            field=models.OneToOneField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='confectionary', to=settings.AUTH_USER_MODEL),
        ),
    ]
