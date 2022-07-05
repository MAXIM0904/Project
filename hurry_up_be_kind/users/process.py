import os.path
from .models import UserData, AvatarUser
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import ImgForm
from random import randint
import requests
import json


def _create_user(serializer_form):
    """
    Функция сохранения данных пользователя в базу данных.
    Сохраняет номер телефона в username.
    """
    random = _random_int()
    email = ''
    if serializer_form.validated_data.get('email'):
        email = serializer_form.validated_data['email']

    create_user = UserData.objects.create_user(
        username=serializer_form.validated_data['phone'],
        phone=serializer_form.validated_data['phone'],
        email= email,
        status=serializer_form.validated_data['status'].lower(),
        first_name=serializer_form.validated_data['first_name'],
        last_name=serializer_form.validated_data['last_name'],
        patronymic=serializer_form.validated_data['patronymic'],
        password=serializer_form.validated_data['password'],
        random_number=int(random),

    )
    _sending_sms(user=create_user)
    return create_user


def _message_user(user, flag):
    if flag:
        return 'Ваш профиль активирован. Войдите в приложение фонда "Скорей добрей"'
    return user.random_number


def _sending_sms(user, flag=None):
    ''' Функция отправки СМС пользователю '''
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
    '''Функция генерирует случайное четырехзначное число'''
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
        list_files.append(f'{i_file}')
    return list_files


def _inf_user(request):
    """ Функция возвращает информацию о пользователе """
    file_user = _file_get(request=request)
    status = request.user.status
    context = {'last_name': request.user.last_name,
               'first_name': request.user.first_name,
               'patronymic': request.user.patronymic,
               'phone': request.user.phone,
               'email': request.user.email,
               'address_ward': request.user.address_ward,
               'about_me': request.user.about_me,
               'avatar_user': str(request.user.avatar_user),
               'link_user_files': file_user,
               'status': status,
               }

    if status in ['philantropist', 'confectioner']:
        context['size_donations'] = request.user.size_donations

    return context


def _file_save(request):
    """ Функция массового сохранения картинок """
    form_img = ImgForm(request.POST, request.FILES)
    if form_img.is_valid():
        files = form_img.files.getlist('save_file')

        for i_files in files:
            file_instanse = AvatarUser(model_file=request.user, file_user=i_files)
            file_instanse.save()
        return True

    raise TypeError('no files found')


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
    """ Функция удаления картинки """
    for i_img in url_img:
        if os.path.isfile(i_img):
            os.remove(i_img)
    return True


def _delete_user(request):
    """ Функция удаления пользователя из базы данных """
    user_profile = UserData.objects.get(id=request.user.id)
    user_file = _file_get(request)
    _delete_img(user_file)
    user_profile.delete()
    return True


def _verification_code(user, verification_code):
    random_code = int(user.random_number)
    if verification_code == random_code and random_code != 0:
        user.random_number = 0
        user.save()
        return True
    else:
        raise TypeError('Код не совпадает')



def _verification_user(user, verification_code):
    ''' Функция проверки совпадает ли код введенный пользователем с кодом сгенерированным программой '''
    if _verification_code(user=user, verification_code=verification_code):
        if user.status == "ward":
            return {
                'registration': 'True',
                'message': 'Дождитесь подтверждения профиля администратором'
            }
        user.is_active = True
        user.save()
        jwt_token = _get_tokens_for_user(user=user)
        return jwt_token
