from .models import UserData
from rest_framework_simplejwt.tokens import RefreshToken


def _create_user(serializer_form):
    """
    Функция сохранения данных пользователя в базу данных.
    Сохраняет номер телефона в username.
    """
    create_user = UserData.objects.create_user(
        username=serializer_form.validated_data['phone'],
        phone=serializer_form.validated_data['phone'],
        status=serializer_form.validated_data['status'].lower(),
        first_name=serializer_form.validated_data['first_name'],
        last_name=serializer_form.validated_data['last_name'],
        password=serializer_form.validated_data['password'],
    )
    return create_user


def _get_tokens_for_user(user):
    """ Функция выдачи JWT токена """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def _inf_user(request):
    """ Функция возвращает информацию о пользователе """
    status = request.user.status
    if status in ['philantropist', 'confectioner', 'ward']:
        context = {'last_name': request.user.last_name,
                   'first_name': request.user.first_name,
                   'phone': request.user.phone,
                   'about_me': request.user.about_me,
                   'link_user_img': '',
                   'status': status,
                   }

        if status == 'philantropist':
            context['size_donations'] = request.user.size_donations

        return context

    else:
        raise ValueError('The status does not exist')


def _save_data_user(request, user_form):
    """
    Функция сохраняет измененную информацию о пользователе
    В случае замены 'phone' изменяется и username.
    """
    if user_form.validated_data.get('phone'):
        request.user.username = user_form.validated_data['phone']
    user_form.save()
    return True


def _delete_user(request):
    """ Функция удаления пользователя из базы данных """
    user_profile = UserData.objects.get(id=request.user.id)
    user_profile.delete()
    return True
