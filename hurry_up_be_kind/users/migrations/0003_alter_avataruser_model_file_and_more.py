# Generated by Django 4.0.4 on 2022-05-04 12:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_avataruser_remove_userdata_avatar_user_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avataruser',
            name='model_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userdata',
            name='size_donations',
            field=models.IntegerField(default=0, verbose_name='Размер пожертвований'),
        ),
    ]
