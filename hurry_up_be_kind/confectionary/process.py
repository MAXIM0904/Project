import os

from django.contrib.auth.hashers import make_password
from .models import Confectionary, ImgFileConfectionary
from .forms import ImgConfectionaryForm
from .serializers import ConfectionarySerializer, ConfectionaryAllSerializer
from django.contrib.auth import authenticate


def _confectionary_save(request, confectionary_data):
    """Функция сохранения кондитерской с картинками"""
    confectionary_name = ''
    number_phone = ''
    address_ward = ''
    description_confectionary = ''
    if confectionary_data.get('confectionary_name'):
        confectionary_name = confectionary_data['confectionary_name']
    if confectionary_data.get('number_phone'):
        number_phone = confectionary_data['number_phone']
    if confectionary_data.get('address_ward'):
        address_ward = confectionary_data['address_ward']
    if confectionary_data.get('description_confectionary'):
        description_confectionary = confectionary_data['description_confectionary']

    instance = Confectionary.objects.create(
        director=request.user,
        confectionary_name=confectionary_name,
        number_phone=number_phone,
        address_ward=address_ward,
        description_confectionary=description_confectionary
    )

    if confectionary_data.get('img_confectionary'):
        _image_save(instance=instance, request=request)

    return instance


def _update_img(request, instance, user_form):
    """Функция сохранения картинок"""
    if user_form.validated_data.get('img_confectionary'):
        _image_save(request=request, instance=instance)
        return True

    else:
        return True



def _image_save(request, instance):
    """ Функция массового сохранения картинок """
    form_img = ImgConfectionaryForm(request.POST, request.FILES)
    if form_img.is_valid():
        images = form_img.files.getlist('img_confectionary')
        for i_image in images:
            file_instanse = ImgFileConfectionary(file_confectionary=instance, img_confectionary=i_image)
            file_instanse.save()
        return True

    raise TypeError('no image found')


def _image_get(instance):
    """ Функция возвращает список адресов картинок пользователя """
    list_images = []
    image_user = instance.file_confectionary.all()
    for i_image in image_user:
        list_images.append(f'{i_image}')
    return list_images



def _inf_confectionary(instance):
    """ Функция возвращает информацию о пользователе адресов картинок пользователя """
    inf_confectionary = ConfectionaryAllSerializer(instance)
    inf_confectionary = inf_confectionary.data
    img_confectionary = _image_get(instance=instance)
    inf_confectionary['img_confectionary'] = img_confectionary
    return inf_confectionary


def _delete_img(url_img):
    """ Функция удаления картинки """
    for i_img in url_img:
        if os.path.isfile(i_img):
            os.remove(i_img)
    return True


def _delete_confectionary(request):
    """ Функция удаления пользователя из базы данных """
    user_profile = request.user.confectionary
    user_file = _image_get(instance=user_profile)
    _delete_img(user_file)
    user_profile.delete()
    return True
