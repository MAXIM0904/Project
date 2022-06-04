import os.path
from .models import UserData, AvatarUser
from rest_framework_simplejwt.tokens import RefreshToken
from .forms import ImgForm
from random import randint
from base64 import b64encode
import requests
import json


def _create_user(serializer_form):
    """
    Функция сохранения данных пользователя в базу данных.
    Сохраняет номер телефона в username.
    """
    random = _random_int()
    create_user = UserData.objects.create_user(
        username=serializer_form.validated_data['phone'],
        phone=serializer_form.validated_data['phone'],
        status=serializer_form.validated_data['status'].lower(),
        first_name=serializer_form.validated_data['first_name'],
        last_name=serializer_form.validated_data['last_name'],
        password=serializer_form.validated_data['password'],
        random_number=int(random),
    )
    _sending_sms(user=create_user)
    return create_user


def _sending_sms(user):
    ''' Функция отправки СМС пользователю '''
    number = user.username
    login = os.environ.get("login_sms")
    password = os.environ.get("password_sms")
    random_number = user.random_number

    url = 'https://omnichannel.mts.ru/http-api/v1/messages'
    bit_password = b64encode(bytes(f"{login}:{password}", "utf-8")).decode("ascii")

    headers = {
        "Authorization": f"Basic {bit_password}",
        "Content-Type": "application/json"
    }
    payload = json.dumps({
        "messages": [
            {
                "content": {
                    "short_text": f"{random_number}"
                },
                "from": {
                    "sms_address": "MTSM_Test"
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
    # _sending_sms(user=user, random_number=random_number)


def _get_tokens_for_user(user):
    """ Функция выдачи JWT токена """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def _image_get(request):
    """ Функция возвращает список адресов картинок пользователя """
    list_images = []
    image_user = request.user.model_file.all()
    for i_image in image_user:
        list_images.append(f'images/{i_image}')
    return list_images


def _inf_user(request):
    """ Функция возвращает информацию о пользователе """
    image_user = _image_get(request=request)
    status = request.user.status

    context = {'last_name': request.user.last_name,
               'first_name': request.user.first_name,
               'phone': request.user.phone,
               'about_me': request.user.about_me,
               'link_user_img': image_user,
               'address_ward': request.user.address_ward,
               'status': status,
               }

    if status == 'philantropist':
        context['size_donations'] = request.user.size_donations

    return context


def _image_save(request):
    """ Функция массового сохранения картинок """
    form_img = ImgForm(request.POST, request.FILES)
    if form_img.is_valid():
        images = form_img.files.getlist('image')

        for i_image in images:
            file_instanse = AvatarUser(model_file=request.user, avatar_user_img=i_image)
            file_instanse.save()
        return True

    else:
        raise TypeError({'error': 'no image found'})


def _save_data_user(request, user_form):
    """
    Функция сохраняет измененную информацию о пользователе
    В случае замены 'phone' изменяется и username.
    """
    if user_form.validated_data.get('phone'):
        request.user.username = user_form.validated_data['phone']

    if user_form.validated_data.get('image'):
        _image_save(request=request)

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
    user_file = _image_get(request)
    _delete_img(user_file)
    user_profile.delete()
    return True
