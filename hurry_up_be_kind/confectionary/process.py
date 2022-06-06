from django.contrib.auth.hashers import make_password
from .models import Confectionary, ImgFileConfectionary
from .forms import ImgConfectionaryForm
from .serializers import ConfectionarySerializer
from django.contrib.auth import authenticate


def _file_confectionary_save(instance, request):
    """ Функция массового сохранения картинок """
    form_img = ImgConfectionaryForm(request.POST, request.FILES)
    if form_img.is_valid():
        images = form_img.files.getlist('img_confectionary')
        for i_image in images:
            file_instanse = ImgFileConfectionary(file_confectionary=instance, img_confectionary=i_image)
            file_instanse.save()
        return True

    else:
        raise TypeError({'error': 'no image found'})


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
        _file_confectionary_save(instance=instance, request=request)

    return True
