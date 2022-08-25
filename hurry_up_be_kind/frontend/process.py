import requests
from django.http import HttpResponseNotFound
from . import requests_to_the_server
from django.shortcuts import redirect


menu_home_page = {
    'user_out_logging': [
        {'title': 'Вход', 'url_name': 'hurry_up_be_kind:logging_user', 'method': 'GET'},
        {'title': 'Регистрация', 'url_name': 'hurry_up_be_kind:registration', 'method': 'GET'}
    ],

    'user_logging': [
        {'title': 'Личный кабинет', 'url_name': 'hurry_up_be_kind:getting_your_data', 'method': 'GET'},
        {'title': 'Меню', 'url_name': 'hurry_up_be_kind:menu_list', 'method': 'GET'},
        {'title': 'Моя корзина', 'url_name': 'hurry_up_be_kind:all_order', 'method': 'GET'},
        {'title': 'Выход', 'url_name': 'hurry_up_be_kind:logout', 'method': 'GET'}
    ],

    'user_confectionary_logging': [
        {'title': 'Регистрация кондитерской', 'url_name': 'hurry_up_be_kind:registration_confectionary', 'method': 'GET'},
        {'title': 'Заказы кондитерской', 'url_name': 'hurry_up_be_kind:all_order_confectionary', 'method': 'GET'},
        {'title': 'Моя кондитерская', 'url_name': 'hurry_up_be_kind:pastry_shop_office', 'method': 'GET'},
    ],

    'is_admin': [
        {'title': 'Массовая загрузка меню', 'url_name': 'hurry_up_be_kind:bulk_loading_menu', 'method': 'GET'},
    ]
}


def token_update(request, dict_response, redirect_urls):
    """Функция обновляет токен и создает сессию для снижения количества запросов к серверу"""
    access_token_life = 60 * 60 * 22
    refresh_token_life = 60 * 60 * 24 * 5

    if 'access' in dict_response:
        response = redirect(redirect_urls)
        response.set_cookie('refresh', dict_response['refresh'], max_age=refresh_token_life)
        response.set_cookie('access', dict_response['access'], max_age=access_token_life)
        request.session.set_expiry(access_token_life)
        request.session['pause'] = True
        return response
    return False


def controll_context(request, title, form=None):
    context = {
        'title': title,
        'form': form,
        'menu': token_control(request)
    }
    return context


def token_control(request):
    if 'pause' not in request.session:
        token_refresh = request.COOKIES.get('refresh')
        if token_refresh is not None:
            payload = {
                'refresh': token_refresh
            }
            dict_response = requests_to_the_server.urls_request(key_request='token_update', payload=payload)
            token_update(request=request, dict_response=dict_response, redirect_urls='/hurry_up_be_kind/index')

        return menu_home_page['user_out_logging']
    else:
        return menu_home_page['user_logging']


def delete_cookie(request):
    response = redirect('/hurry_up_be_kind/index')
    response.delete_cookie('refresh')
    response.delete_cookie('access')
    response.delete_cookie('id')
    response.delete_cookie('sessionid')
    return response


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')

#
# def preparation_for_html(dict_response):
#     """
#     Функция преобразует поступивший словарь с информацией о пользователе во вложенный список
#     для дальнейшего использования в html странице.
#     Английские значения словаря заменяются на русские.
#
#     """
#     categories = {
#         'last_name': 'Фамилия',
#         'first_name': 'Имя',
#         'patronymic': 'Отчество',
#         'phone': 'Номер телефона',
#         'email': 'Электронная почта',
#         'address_ward': 'Адрес',
#         'about_me': 'Обо мне',
#         'avatar_user': 'Аватар',
#         'link_user_files': 'Документы',
#         'status': 'Статус',
#         'size_donations': 'Сумма донатов'
#     }
#
#     user_status = {
#         "philantropist": "благотворитель",
#         "ward": "подопечный",
#         "confectioner": "кондитер",
#     }
#     status = dict_response['status']
#     dict_response['status'] = user_status[status]
#
#     return dict_response
