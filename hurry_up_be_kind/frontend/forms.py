from django import forms
from users.models import UserData
from confectionary.models import Confectionary
from django.contrib.auth.forms import UserCreationForm


# User
class RegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices[0] = ('', 'Категория не выбрана')

    save_file = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False, label='Загрузка документов',
        help_text='Поле обязательно, если Вы регистрируетесь как "Подопечный"'
    )
    class Meta:
        model = UserData
        fields = ('first_name', 'last_name', 'patronymic', 'phone', 'email', 'status', 'password1', 'password2', 'save_file',)


class ConfirmationForm(forms.Form):
    verification_code = forms.CharField(label='Код из СМС', max_length=4)


class LoggingForm(forms.Form):
    username = forms.CharField(label='Номер телефона', max_length=14, help_text='Формат ввода номера: 79112223344')
    password = forms.CharField(label='Пароль')

# Confectionary
class RegistrationConfectionaryForm(forms.ModelForm):
    avatar_confectionary = forms.ImageField(label='Фото кондитерской', required=False)

    class Meta:
        model = Confectionary
        fields = ('confectionary_name', 'number_phone', 'description_confectionary',
                  'address_ward', 'avatar_confectionary')

# Menu
class BulkLoadingMenuForm(forms.Form):
    menu_file = forms.FileField(
        label='Загрузка меню',
        help_text='Формат файла для загрузки - .xlsx. Содержание файла строго в соответствии с установленой формой.'
    )
