import os.path
from .models import UserData, FileUser
from rest_framework_simplejwt.tokens import RefreshToken
from hurry_up_be_kind.settings import MEDIA_URL
from .serializers import UserRegistrationSerializer
from .forms import FileForm
from random import randint
import requests
import json



def _create_user(request):
    """
    Функция сохранения данных пользователя в базу данных.
    Сохраняет номер телефона в username.
    """
    random = _random_int()
    email = ''
    serializer_form = UserRegistrationSerializer(data=request.data)

    serializer_form.is_valid(raise_exception=True)

    if serializer_form.validated_data.get('email'):
        email = serializer_form.validated_data['email']

    status_user = serializer_form.validated_data['status']

    if status_user == 'ward':
        if not serializer_form.validated_data.get('save_file'):
            raise ValueError('Необходимо загрузить документы.')

    create_user = UserData.objects.create_user(
        username=serializer_form.validated_data['phone'],
        phone=serializer_form.validated_data['phone'],
        email=email,
        status=status_user,
        first_name=serializer_form.validated_data['first_name'],
        last_name=serializer_form.validated_data['last_name'],
        patronymic=serializer_form.validated_data['patronymic'],
        password=serializer_form.validated_data['password'],
        random_number=int(random),
    )

    if status_user == 'ward':
        _file_save(request=request, user_instanse=create_user)
    _sending_sms(user=create_user)

    return create_user


def _message_user(user, flag):
    """
    Функция по флагу определяет нужен ли random_number.
    1. Если флага нет - выдается random_number
    2. Если флаг есть - выдается сообщение, что профиль активирован.
    """
    if flag:
        return 'Ваш профиль активирован. Войдите в приложение фонда "Скорей добрей"'
    return user.random_number


def _sending_sms(user, flag=None):
    """ Функция отправки СМС пользователю """
    number = user.username
    message_number = _message_user(user=user, flag=flag)

    url = 'https://omnichannel.mts.ru/http-api/v1/messages'

    headers = {
        "Authorization": "Basic Z3dfaGtOUTVNb3k4ZFB2OmIxY0RMR3dr",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "messages": [
            {
                "content": {
                    "short_text": f"{message_number}"
                },
                "from": {
                    "sms_address": "SkoreiDobre"
                },
                "to": [
                    {
                        "msisdn": f"{number}"
                    }
                ]
            }
        ]
    })

    # response = requests.request("POST", url, headers=headers, data=payload)
    # print(response.text)


def _random_int():
    """ Функция генерирует случайное четырехзначное число """
    random_number = randint(1000, 9999)
    return random_number


def _get_tokens_for_user(user):
    """ Функция выдачи JWT токена """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def _file_get(request):
    """ Функция возвращает список файлов пользователя """
    list_files = []
    file_user = request.user.model_file.all()
    for i_file in file_user:
        list_files.append(f'{request._current_scheme_host}{MEDIA_URL}{i_file}')
    return list_files


def _inf_user(request):
    """ Функция возвращает информацию о пользователе """
    file_user = _file_get(request=request)

    if request.user.avatar_user:
        avatar_user = f"{request._current_scheme_host}{request.user.avatar_user.url}"
    else:
        avatar_user = ''

    status = request.user.status
    context = {'last_name': request.user.last_name,
               'first_name': request.user.first_name,
               'patronymic': request.user.patronymic,
               'phone': request.user.phone,
               'email': request.user.email,
               'address_ward': request.user.address_ward,
               'about_me': request.user.about_me,
               'avatar_user': avatar_user,
               'link_user_files': file_user,
               'status': status,
               }

    if status in ['philantropist', 'confectioner']:
        context['size_donations'] = request.user.size_donations
    return context


def _file_save(request, user_instanse=None):
    """ Функция массового сохранения файлов """
    if user_instanse:
        user_profile = user_instanse
    else:
        user_profile = request.user
    form_file = FileForm(request.POST, request.FILES)
    if form_file.is_valid():
        files = form_file.files.getlist('save_file')
        for i_files in files:
            file_instanse = FileUser(model_file=user_profile, file_user=i_files)
            file_instanse.save()
        return True

    raise TypeError('файлы не найдены')


def _save_data_user(request, user_form):
    """
    Функция сохраняет измененную информацию о пользователе
    В случае замены 'phone' изменяется и username.
    """
    if user_form.validated_data.get('phone'):
        request.user.username = user_form.validated_data['phone']

    if user_form.validated_data.get('save_file'):
        _file_save(request=request)

    user_form.save()
    return True


def _delete_img(url_img):
    """ Функция удаления файла """
    for i_img in url_img:
        if os.path.isfile(i_img):
            os.remove(i_img)
            return True
    return 'Файлов нет'


def _delete_user(request):
    """ Функция удаления пользователя из базы данных """
    user_profile = UserData.objects.get(id=request.user.id)
    user_file = _file_get(request)
    _delete_img(user_file)
    user_profile.delete()
    return True


def _verification_code(user, verification_code):
    """ Функция проверки равенства введенного кода и сгенерированного """
    random_code = int(user.random_number)
    if verification_code == random_code and random_code != 0:
        user.random_number = 0
        user.save()
        return True
    else:
        raise TypeError('Код не совпадает')


def _verification_user(user, verification_code):
    """ Функция выдачи токенов и активации ward """
    if _verification_code(user=user, verification_code=verification_code):
        if user.status == "ward":
            return {
                'registration': 'True',
                'message': ' Вы успешно подтвердили номер телефона. Дождитесь подтверждения профиля администратором'
            }
        user.is_active = True
        user.save()
        jwt_token = _get_tokens_for_user(user=user)
        return jwt_token
