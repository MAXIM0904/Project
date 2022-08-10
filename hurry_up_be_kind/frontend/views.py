from django.http import HttpResponseNotFound
from django.shortcuts import render
from .forms import RegistrationForm, ConfirmationForm, LoggingForm, RegistrationConfectionaryForm
from django.shortcuts import redirect
from . import process
from . import requests_to_the_server


def index(request):
    menu = ['об организации', 'проекты', 'как помочь', 'контакты']
    return render(request, 'frontend/homepage.html', {'title': 'Главная страница', 'menu': menu})


def registration(request):
    if request.method == "GET":
        form = RegistrationForm()
        return render(request, 'frontend/registration.html', {'form': form, 'title': 'Страница регистрации'})

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
            dict_response = requests_to_the_server.urls_request(key_request='registration', payload=payload, files=files)

            if dict_response['registration'] == 'True':
                response = redirect('/hurry_up_be_kind/sms_confirmation')
                response.set_cookie('id', dict_response['id'], max_age=90000)
                return response

            elif dict_response['registration'] == 'error':
                errors = dict_response['id']
                return render(request, 'frontend/registration.html', {'form': form, 'errors': errors})

        return render(request, 'frontend/registration.html', {'form': form})


def sms_confirmation(request):
    if request.method == "GET":
        form = ConfirmationForm()
        return render(request, 'frontend/sms_confirmation.html', {'form': form})

    elif request.method == "POST":
        id_user = request.COOKIES.get('id')

        if id_user is None:
            return HttpResponseNotFound('Все сломалось. А должна быть функция отправки повторного кода подтверждения.')

        payload = {'id': id_user,
                   'verification_code': request.POST['verification_code'],
                   }
        dict_response = requests_to_the_server.urls_request(key_request='sms_confirmation', payload=payload)

        if 'refresh' in dict_response.keys():
            response = redirect('/hurry_up_be_kind/getting_your_data')
            response.set_cookie('refresh', dict_response['refresh'], max_age=(5 * 24 * 60 * 60))
            response.set_cookie('access', dict_response['access'], max_age=(1 * 24 * 60 * 60))
            return response

        elif 'id' in dict_response.keys():
            form = ConfirmationForm(request.POST)
            errors = dict_response['id']
            return render(request, 'frontend/sms_confirmation.html', {'form': form, 'errors': errors})

        elif 'message' in dict_response.keys():
            message = dict_response['message']
            return render(request, 'frontend/sms_confirmation.html', {'errors': message})


def getting_your_data(request):
    if request.method == "GET":
        access_token = request.COOKIES.get('access')

        if access_token is None:
            return HttpResponseNotFound('Все сломалось. А должна быть функция отправки refresh и записи нового access.')

        headers = {
            'Authorization': f'Token {access_token}'
        }

        dict_response = requests_to_the_server.urls_request(key_request='getting_your_data', headers=headers)

        print(dict_response)

        if 'detail' in dict_response.keys():
            errors = dict_response['detail']
            return render(request, 'frontend/homepage.html', {'errors': errors})

        else:
            dict_response = requests_to_the_server.preparation_for_html(dict_response=dict_response)
            context = {
                'dict_response': dict_response
            }
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

        dict_response = requests_to_the_server.preparation_for_html(dict_response=dict_response)
        context = {
            'dict_response': dict_response
        }
        return render(request, 'frontend/getting_your_data.html', context=context)


def logging_user(request):
    if request.method == "GET":
        form = LoggingForm()
        return render(request, 'frontend/logging_user.html', {'form': form})

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


def registration_confectionary(request):
    if request.method == "GET":
        form = RegistrationConfectionaryForm()
        return render(request, 'frontend/confectionary/confectionary_registration.html', {'form': form})


    elif request.method == "POST":
        form = RegistrationConfectionaryForm(request.POST, request.FILES)
        errors = ''
        if form.is_valid():
            payload = request.POST
            files = request.FILES

            print(request.FILES)
            print(request.POST)

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
        return render(request, 'frontend/confectionary/confectionary_registration.html', {'form': form, 'errors':errors})


def pastry_shop_office(request):
    if request.method == "GET":
        access_token = request.COOKIES.get('access')
        headers = {
            'Authorization': f'Token {access_token}'
        }

        dict_response = requests_to_the_server.urls_request(key_request='inf_confectionary', headers=headers)
        dict_response= requests_to_the_server.confectionary_for_html(dict_response)
        return render(request, 'frontend/confectionary/pastry_shop_office.html', {'dict_response': dict_response})


def update_confectionary(request):

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
        dict_response = requests_to_the_server.confectionary_for_html(dict_response)

        return render(request, 'frontend/confectionary/pastry_shop_office.html', {'dict_response': dict_response})