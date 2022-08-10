import requests
import json

base_urls = 'http://127.0.0.1:8000'

requests_server = {
    'registration':
        {'title': 'Запрос на регистрацию', 'urls': f"{base_urls}/registration_user/", 'method': 'POST'},

    'sms_confirmation':
        {'title': 'Запрос на СМС подтверждение', 'urls': f"{base_urls}/verification_sms/", 'method': 'POST'},

    'getting_your_data':
        {'title': 'Получение своих данных', 'urls': f"{base_urls}/inf_user/", 'method': 'GET'},

    'changing_data':
        {'title': 'Изменение данных', 'urls': f"{base_urls}/update_user/", 'method': 'PATCH'},

    'logging':
        {'title': 'Вход в учетную запись', 'urls': f"{base_urls}/api/token/", 'method': 'POST'},

    'register_confectionary':
        {'title': 'Регистрация кондитерской', 'urls': f"{base_urls}/confectionary/register_confectionary/", 'method': 'POST'},

    'inf_confectionary':
        {'title': 'Информация о кондитерской', 'urls': f"{base_urls}/confectionary/inf_confectionary/", 'method': 'GET'},

    'update_confectionary':
        {'title': 'Изменение данных кондитерской', 'urls': f"{base_urls}/confectionary/update_confectionary/", 'method': 'POST'},

    # Меню
    'update_confectionary':
        {'title': 'Типы меню', 'urls': f"{base_urls}/menu/register_menu/", 'method': 'GET'},




    # 'token_update':
    #     {'title': 'Обновление токена', 'urls': f"{base_urls}api/token/refresh/", 'method': 'POST'},
    #
    #
    # 'password recovery':{
    #     'title': 'Список всех благотворителей(филантропов)', 'urls': f"{base_urls}password_recovery/", 'method': 'POST'
    # },
    #
    # 'deleting_user':
    #     {'title': 'Удаление пользователя', 'urls': f"{base_urls}delete_user/", 'method': 'GET'},
    #
    # 'all users':
    #     {'title': 'Список всех пользователей', 'urls': f"{base_urls}all_user/", 'method': 'GET'},
    #
    # 'all_ward':
    #     {'title': 'Список всех подопечных', 'urls': f"{base_urls}all_ward/", 'method': 'GET'},
    #
    # 'all_philantropist':{
    #     'title': 'Список всех благотворителей(филантропов)', 'urls': f"{base_urls}all_philantropist/", 'method': 'GET'
    # },
}

user_status = {
    "philantropist": "благотворитель",
    "ward": "подопечный",
    "confectioner": "кондитер",
}

def urls_request(key_request, method=None, url=None, payload=None, headers=None, files=None):
    """ Общая функция направления запросов на сервер """
    if method is None:
        method = requests_server[key_request]['method']
    if url is None:
        url = requests_server[key_request]['urls']

    response = requests.request(method=method, url=url, headers=headers, data=payload, files=files)
    dict_response = json.loads(response.text)
    return dict_response


def preparation_for_html(dict_response):
    """
    Функция преобразует поступивший словарь с информацией о пользователе во вложенный список
    для дальнейшего использования в html странице.
    Английские значения словаря заменяются на русские.

    """
    status = dict_response['status']
    dict_response['status'] = user_status[status]
    dict_response['avatar_user'] = f'{base_urls}/images/{dict_response["avatar_user"]}'
    print(dict_response['link_user_files'])
    list_files = []
    for files in dict_response['link_user_files']:
        list_files.append(f'{base_urls}/images/{files}')
    dict_response['link_user_files'] = list_files
    return dict_response


def confectionary_for_html(dict_response):
    """
    Функция преобразует поступивший словарь с информацией о пользователе во вложенный список
    для дальнейшего использования в html странице.
    Английские значения словаря заменяются на русские.

    """

    dict_response['avatar_confectionary'] = f'{base_urls}{dict_response["avatar_confectionary"]}'
    return dict_response