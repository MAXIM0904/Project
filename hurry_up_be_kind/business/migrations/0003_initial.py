# Generated by Django 4.0.4 on 2022-06-10 12:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='basket',
            name='user_philantropist',
            field=models.ManyToManyField(blank=True, related_name='user_philantropist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basket',
            name='user_ward',
            field=models.ManyToManyField(blank=True, related_name='user_ward', to=settings.AUTH_USER_MODEL),
        ),
    ]
