# Generated by Django 4.0.4 on 2022-07-06 08:39

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('phone', models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть введен в формате: '79101111111'. Допускается до 12 цифр.", regex='^\\+?1?\\d{9,12}$')], verbose_name='Номер телефона')),
                ('patronymic', models.CharField(blank=True, max_length=150, null=True, verbose_name='Отчество')),
                ('status', models.CharField(choices=[('philantropist', 'philantropist'), ('ward', 'ward'), ('confectioner', 'confectioner')], max_length=14, verbose_name='Статус пользователя')),
                ('size_donations', models.IntegerField(default=0, verbose_name='Размер пожертвований')),
                ('address_ward', models.TextField(default='', verbose_name='Адрес места нахождения')),
                ('is_active', models.BooleanField(default=False, help_text=('Определяет, следует ли рассматривать этого пользователя как активного. ', 'Отмените выбор этого параметра вместо удаления учетных записей.'), verbose_name='Активность')),
                ('about_me', models.TextField(blank=True, verbose_name='О себе')),
                ('registrarion_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')),
                ('random_number', models.IntegerField(default=0, verbose_name='Код верификации')),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, verbose_name='E-mail')),
                ('avatar_user', models.ImageField(blank=True, null=True, upload_to='avatar_user/', verbose_name='Аватар пользователя')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'пользователя',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['status'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AvatarUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_user', models.FileField(blank=True, upload_to='file_user/', verbose_name='Файлы пользователя')),
                ('model_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='model_file', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'файлы пользователя',
                'verbose_name_plural': 'Файлы пользователей',
            },
        ),
    ]
