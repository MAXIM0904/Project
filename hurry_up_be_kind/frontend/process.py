import requests
from django.http import HttpResponseNotFound
from django.shortcuts import redirect


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена<h1>')



# def del_cookies(request, key_cookies, urls_redirect):
#     cookies_id = request.COOKIES.get(key_cookies)
#     response = redirect(urls_redirect)
#     if cookies_id is not None:
#         response.delete_cookie(key_cookies)
#     return True


# def save_update_cookies(request, key_cookies, urls_redirect, new_cookies, lifetime=None):
#     """ Функция сохраняет куки """
#     cookies_id = request.COOKIES.get(key_cookies)
#     if cookies_id is not None:
#         response = redirect(urls_redirect)
#         response.delete_cookie(key_cookies)
#     response = redirect(urls_redirect)
#     if lifetime is not None:
#         lifetime = lifetime * 24 * 60 * 60
#
#     response.set_cookie(key_cookies, new_cookies, max_age=lifetime)
#     return response


def preparation_for_html(dict_response):
    """
    Функция преобразует поступивший словарь с информацией о пользователе во вложенный список
    для дальнейшего использования в html странице.
    Английские значения словаря заменяются на русские.

    """
    categories = {
        'last_name': 'Фамилия',
        'first_name': 'Имя',
        'patronymic': 'Отчество',
        'phone': 'Номер телефона',
        'email': 'Электронная почта',
        'address_ward': 'Адрес',
        'about_me': 'Обо мне',
        'avatar_user': 'Аватар',
        'link_user_files': 'Документы',
        'status': 'Статус',
        'size_donations': 'Сумма донатов'
    }

    user_status = {
        "philantropist": "благотворитель",
        "ward": "подопечный",
        "confectioner": "кондитер",
    }
    status = dict_response['status']
    dict_response['status'] = user_status[status]
    dict_response['status'] = f''

    return dict_response
