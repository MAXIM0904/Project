from django.http import HttpResponseNotFound
from django.shortcuts import render
from .forms import RegistrationForm, ConfirmationForm, LoggingForm, RegistrationConfectionaryForm, BulkLoadingMenuForm
from django.shortcuts import redirect
from . import requests_to_the_server
from . import process



def index(request):
    """Главная страница"""
    context = process.controll_context(request=request, title='Главная страница')
    return render(request, 'frontend/homepage.html', context=context)


def registration(request):
    """Регистрация пользователя"""
    if request.method == "GET":
        form = RegistrationForm()
        context = process.controll_context(request=request, form=form, title='Страница регистрации')
        return render(request, 'frontend/registration.html', context=context)

    elif request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)

        if request.POST['status'] == 'ward' and request.FILES == {}:
            errors = 'Загрузите документы для подопечного'
            return render(request, 'frontend/registration.html', {'form': form, 'errors': errors})

        if form.is_valid():
            payload = {
                'first_name': form.cleaned_data.get('first_name'),
                'last_name': form.cleaned_data.get('last_name'),
                'patronymic': form.cleaned_data.get('patronymic'),
                'phone': form.cleaned_data.get('phone'),
                'email': form.cleaned_data.get('email'),
                'status': form.cleaned_data.get('status'),
                'password': form.cleaned_data.get('password1'),
            }

            files = request.FILES
            dict_response = requests_to_the_server.urls_request(
                key_request='registration',
                payload=payload,
                files=files
            )

            if dict_response['registration'] == 'True':
                response = redirect('/hurry_up_be_kind/sms_confirmation')
                response.set_cookie('id', dict_response['id'], max_age=90000)
                return response

            elif dict_response['registration'] == 'error':
                errors = dict_response['id']
                return render(request, 'frontend/registration.html', {'form': form, 'errors': errors})

        return render(request, 'frontend/registration.html', {'form': form})


def sms_confirmation(request):
    """СМС подтверждение"""
    if request.method == "GET":
        form = ConfirmationForm()
        context = process.controll_context(request=request, form=form, title='Подтверждение профиля')
        return render(request, 'frontend/sms_confirmation.html', context=context)

    elif request.method == "POST":
        id_user = request.COOKIES.get('id')

        if id_user is None:
            return HttpResponseNotFound('Все сломалось. А должна быть функция отправки повторного кода подтверждения.')

        payload = {'id': id_user, 'verification_code': request.POST['verification_code']}

        dict_response = requests_to_the_server.urls_request(key_request='sms_confirmation', payload=payload)

        if 'refresh' in dict_response.keys():
            response = process.token_update(request=request, dict_response=dict_response, redirect_urls='/hurry_up_be_kind/getting_your_data')
            return response

        elif 'id' in dict_response.keys():
            form = ConfirmationForm(request.POST)
            errors = dict_response['id']
            return render(request, 'frontend/sms_confirmation.html', {'form': form, 'errors': errors})

        elif 'message' in dict_response.keys():
            message = dict_response['message']
            return render(request, 'frontend/sms_confirmation.html', {'errors': message})


def logout(request):
    """Функция выхода из учетной записи"""
    if request.method == "GET":
        response = process.delete_cookie(request)
        return response


def getting_your_data(request):
    """Информация о пользователе"""
    if request.method == "GET":
        access_token = request.COOKIES.get('access')

        if access_token is None:
            return HttpResponseNotFound('Все сломалось. А должна быть функция отправки refresh и записи нового access.')

        headers = {
            'Authorization': f'Token {access_token}'
        }
        dict_response = requests_to_the_server.urls_request(key_request='getting_your_data', headers=headers)


        if 'detail' in dict_response.keys():
            errors = dict_response['detail']
            return render(request, 'frontend/homepage.html', {'errors': errors})

        else:
            # dict_response = requests_to_the_server.preparation_for_html(dict_response=dict_response)
            context = process.controll_context(request=request, title='Личный кабинет')
            context['dict_response'] = dict_response
            return render(request, 'frontend/getting_your_data.html', context=context)


def changing_data(request):

    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        payload = request.POST
        headers = {
            'Authorization': f'Token {access_token}'
        }

        dict_response = requests_to_the_server.urls_request(
            key_request='changing_data', payload=payload, headers=headers
        )

        requests_to_the_server.preparation_for_html(dict_response=dict_response)

        return redirect('/hurry_up_be_kind/getting_your_data')



def logging_user(request):
    """Функция входа в учетную запись"""
    if request.method == "GET":
        form = LoggingForm()
        context = process.controll_context(request=request, form=form, title='Вход в учетную запись')
        return render(request, 'frontend/logging_user.html', context=context)

    if request.method == "POST":
        form = LoggingForm(request.POST)
        if form.is_valid():
            payload = request.POST
            dict_response = requests_to_the_server.urls_request(key_request='logging', payload=payload)
            if 'refresh' in dict_response.keys():
                response = redirect('home_page')
                response.set_cookie('refresh', dict_response['refresh'], max_age=(5 * 24 * 60 * 60))
                response.set_cookie('access', dict_response['access'], max_age=(1 * 24 * 60 * 60))
                return response
            else:
                errors = 'Введенные данные не верны'
                return render(request, 'frontend/logging_user.html', {'form': form, 'errors': errors})


def all_ward(request):
    """Функция выбора всех подопечных """

    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }
        dict_response = requests_to_the_server.urls_request(key_request='all_ward', headers=headers)
        order_id = request.POST['order_id']
        context = process.controll_context(request=request, title='Выбор подопечного')
        context['dict_response'] = dict_response
        context['order_id'] = order_id
        return render(request, 'frontend/all_ward.html', context=context)


def registration_confectionary(request):
    """Функция регистрации кондитерской"""
    if request.method == "GET":
        form = RegistrationConfectionaryForm()
        context = process.controll_context(request=request, form=form, title='Регистрация кондитерской')
        return render(request, 'frontend/confectionary/confectionary_registration.html', context=context)


    elif request.method == "POST":
        form = RegistrationConfectionaryForm(request.POST, request.FILES)
        errors = ''
        if form.is_valid():
            payload = request.POST
            files = request.FILES

            access_token = request.COOKIES.get('access')

            headers = {
                'Authorization': f'Token {access_token}'
            }
            dict_response = requests_to_the_server.urls_request(
                key_request='register_confectionary', payload=payload, headers=headers, files=files
            )
            if 'detail' in dict_response.keys():
                errors = dict_response['detail']

            elif 'registration' in dict_response.keys():
                if dict_response['registration'] == 'error':
                    errors = dict_response['id']
                    return render(
                        request, 'frontend/confectionary/confectionary_registration.html', {
                            'form': form,
                            'errors': errors
                        }
                    )

            elif 'number_phone' in dict_response.keys():
                return redirect('/hurry_up_be_kind/pastry_shop_office')
        return render(request, 'frontend/confectionary/confectionary_registration.html', {
            'form': form,
            'errors': errors
        })


def pastry_shop_office(request):
    """Функция вывода информации о кондитерской"""
    if request.method == "GET":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        dict_response = requests_to_the_server.urls_request(key_request='inf_confectionary', headers=headers)
        # dict_response= requests_to_the_server.confectionary_for_html(dict_response)

        context = process.controll_context(request=request, title='Личный кабинет кондитерской')
        context['dict_response'] = dict_response
        print(dict_response)
        return render(request, 'frontend/confectionary/pastry_shop_office.html', context=context)


def update_confectionary(request):
    """Функция изменения данных кондитерской"""
    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        payload = request.POST
        files = request.FILES

        dict_response = requests_to_the_server.urls_request(
            key_request='update_confectionary', headers=headers, payload=payload, files=files
        )
        requests_to_the_server.confectionary_for_html(dict_response)

        return redirect('/hurry_up_be_kind/pastry_shop_office')





def all_confectionary(request):
    """Функция выводит все кондитеpские """

    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }
        dict_response = requests_to_the_server.urls_request(
                    key_request='all_confectionary', headers=headers)
        order_id = request.POST['order_id']

        return render(request, 'frontend/confectionary/all_confectionary.html', {
            'dict_response': dict_response,
            'order_id': order_id,
        })



#menu
def menu_list(request):
    """ Функция вывода меню эконом, оптимального и бизнес """
    if request.method == "GET":
        context = process.controll_context(request=request, title='Меню')
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }
        menu = 'all_optimal_menu'
        name_menu = 'Оптимальное меню'
        if 'orderby' in request.GET.keys():
            menu = request.GET['orderby']

            if request.GET['orderby'] == 'all_economy_menu':
                name_menu = 'Экономное меню'

            elif request.GET['orderby'] == 'all_business_menu':
                name_menu = 'Бизнес меню'

        dict_response = requests_to_the_server.urls_request(key_request=menu, headers=headers)
        context['dict_response'] = dict_response
        context['name_menu'] = name_menu
        return render(request, 'frontend/menu/menu_list.html', context=context)


def bulk_loading_menu(request):
    """ Функция массового добавления меню """
    if request.method == "GET":
        form = BulkLoadingMenuForm()
        return render(request, 'frontend/menu/bulk_loading_menu.html', {'form': form})


    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        form = BulkLoadingMenuForm(request.POST, request.FILES)

        if form.is_valid():
            files = request.FILES
            dict_response = requests_to_the_server.urls_request(
                key_request='massive_menu_update', headers=headers, files=files
            )

            if 'registration' in dict_response.keys():
                if dict_response['registration'] == 'error':
                    return render(
                        request, 'frontend/menu/bulk_loading_menu.html', {'form': form, 'dict_response': dict_response}
                    )

                elif dict_response['registration'] == 'True':
                    return redirect('/hurry_up_be_kind/menu_list')

        else:
            return render(request, 'frontend/menu/bulk_loading_menu.html', {'form': form})


# корзина
def order(request):
    """ Функция добавления в корзину """
    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        payload = request.POST

        dict_response = requests_to_the_server.urls_request(
            key_request='order', headers=headers, payload=payload
        )
        context = process.controll_context(request=request, title='Доброе дело')
        context['dict_response'] = dict_response
        return render(request, 'frontend/business/order.html', context=context)


def update_order(request):
    """ Функция изменения корзины """
    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        payload = request.POST
        dict_response = requests_to_the_server.urls_request(
            key_request='update_order', headers=headers, payload=payload
        )
        context = process.controll_context(request=request, title='Доброе дело')
        context['dict_response'] = dict_response

        return render(request, 'frontend/business/order.html', context=context)


def payment(request):
    """ Функция оплаты заказа """
    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        payload = request.POST

        dict_response = requests_to_the_server.urls_request(
            key_request='payment', headers=headers, payload=payload
        )
        context = process.controll_context(request=request, title='Доброе дело')
        context['dict_response'] = dict_response
        return render(request, 'frontend/business/order.html', context=context)


def all_order(request):
    """ Функция возвращает все товары в корзине """
    if request.method == "GET":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        dict_response = requests_to_the_server.urls_request(key_request='all_order', headers=headers)
        context = process.controll_context(request=request, title='Корзина')
        context['dict_response'] = dict_response
        return render(request, 'frontend/business/order_all.html', context=context)


def all_order_confectionary(request):
    """ Функция возвращает все заказы кондитерской """
    if request.method == "GET":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        dict_response = requests_to_the_server.urls_request(key_request='all_order_confectionary', headers=headers)
        return render(request, 'frontend/business/all_order_confectionary.html', {'dict_response': dict_response})


def all_desire_ward(request):
    """ Функция возвращает все желания подопечного """
    if request.method == "GET":
        access_token = request.COOKIES.get('access')
        # headers = {
        #     'Authorization': f'Token {access_token}'
        # }

        dict_response = requests_to_the_server.urls_request(key_request='all_desire_ward')
        context = process.controll_context(request=request, title='Желания подопечного')
        context['dict_response'] = dict_response
        return render(request, 'frontend/business/desire_ward.html', context=context)


def execute_an_order(request):
    """ Функция позволяет поставить статус заказа - выполнен """
    if request.method == "POST":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }
        payload = request.POST

        dict_response = requests_to_the_server.urls_request(
            key_request='execute_an_order', headers=headers, payload=payload
        )
        return redirect('/hurry_up_be_kind/all_order_confectionary')

