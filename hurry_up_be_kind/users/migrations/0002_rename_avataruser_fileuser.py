# Generated by Django 4.0.4 on 2022-07-23 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AvatarUser',
            new_name='FileUser',
        ),
    ]
