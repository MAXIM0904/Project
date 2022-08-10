import tempfile
import os.path
import json
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIRequestFactory, APIClient
from django.urls import reverse
from users.models import UserData, FileUser
from rest_framework_simplejwt.tokens import RefreshToken


class TestFunctions(APITestCase):

    def test_home_page_urls_reverse(self):
        """
        Тестирование перехода на главную страницу сайта urls reverse
        """
        resp = self.client.get(reverse('home_page'))
        self.assertEqual(resp.status_code, 301)


    def test_home_page_urls(self):
        """
        Тестирование перехода на главную страницу сайта urls
        """
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 301)



class TestRegistrationUser(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        avatar = tempfile.NamedTemporaryFile(suffix='.jpg').name

        self.data_user = {
            'username': 'TestUsername',
            'phone': '79101111111',
            'email': 'jkljkkl@mail.ru',
            'status': 'ward',
            'first_name': 'TestFirst_name',
            'last_name': 'TestLast_name',
            'patronymic': 'TestPatronymic',
            'password': 'TestPassword',
            'avatar_user': avatar
        }

    def test_registration_user_urls_reverse(self):
        """
        Тестирование адреса регистрации пользователя urls reverse
        """
        resp = self.client.post(reverse('registration_user'))
        self.assertEqual(resp.status_code, 200)

    def test_registration_user_urls(self):
        """
        Тестирование адреса регистрации пользователя urls
        """
        resp = self.client.post('/registration_user/')
        self.assertEqual(resp.status_code, 200)

    def test_registration_user_ward_valid(self):
        """
        Тестирование регистрации валидных данных ward.
        """
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.data_user['save_file'] = file
        resp = self.client.post(reverse('registration_user'), data=self.data_user, format='multipart')
        self.assertEqual(resp.status_code, 200)
        resp = json.loads(resp.content)
        self.assertEqual(len(resp), 2)
        self.assertEqual(resp['registration'], 'True')
        self.assertEqual(list(resp.keys()), ['registration', 'id'])
        user_profile = UserData.objects.filter(phone='79101111111')
        self.assertEqual(len(user_profile), 1)
        self.assertEqual(user_profile[0].status, 'ward')
        self.assertEqual(user_profile[0].is_active, False)

        if os.path.exists(f'images/file_user/{file.name}'):
            os.remove(f'images/file_user/{file.name}')

    def test_registration_user_philantropist(self):
        """ Тестирование регистрации валидных данных philantropist """
        self.data_user['status'] = 'philantropist'
        resp = self.client.post(reverse('registration_user'), data=self.data_user, format='multipart')
        self.assertEqual(resp.status_code, 200)
        resp = json.loads(resp.content)
        self.assertEqual(len(resp), 2)
        self.assertEqual(resp['registration'], 'True')
        self.assertEqual(list(resp.keys()), ['registration', 'id'])
        user_profile = UserData.objects.filter(phone='79101111111')
        self.assertEqual(user_profile.count(), 1)
        self.assertEqual(user_profile[0].status, 'philantropist')
        self.assertEqual(user_profile[0].is_active, False)


class TestInfUser(APITestCase):

    def setUp(self):
        self.user = UserData.objects.create_user(username='TestUsername1', password='123456')

    def test_inf_user_urls_reverse_philantropist(self):
        """
        Тестирование адреса регистрации пользователя urls reverse
        Тестирование получения информации о пользователе philantropist
        """
        self.user.status = 'philantropist'
        self.user.is_active = True
        self.user.save()
        token = RefreshToken.for_user(self.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.access_token}")

        resp = client.get('/inf_user/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        resp = json.loads(resp.content)
        self.assertEqual(len(resp), 11)

    def test_inf_user_urls_ward(self):
        """
        Тестирование адреса регистрации пользователя urls
        Тестирование получения информации о пользователе ward
        """
        # user = UserData.objects.create_user(username='TestUsername1', password='123456')
        self.user.status = 'ward'
        self.user.is_active = True
        self.user.save()
        token = RefreshToken.for_user(self.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {token.access_token}")

        resp = client.get(reverse('inf_user'), data={'format': 'json'})
        self.assertEqual(resp.status_code, 200)
        resp = json.loads(resp.content)
        self.assertEqual(len(resp), 10)

    def test_inf_user_token_invalid(self):
        """
        Тестирование НЕ валидного токена
        """

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f"Token {'123458'}")

        resp = client.get('/inf_user/', data={'format': 'json'})
        self.assertEqual(resp.status_code, 401)
