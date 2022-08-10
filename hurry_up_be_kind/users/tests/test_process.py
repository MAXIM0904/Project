import os.path
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIRequestFactory
from users.serializers import UserUpdateSerializer
from users.models import UserData, FileUser
from users import process
import tempfile


class TestCreateUser(APITestCase):

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

    def test_create_user_ward_valid(self):
        """
        Тестирование передачи валидных данных ward.
        """
        file = SimpleUploadedFile("file.txt", b"file_content")
        self.data_user['save_file'] = file
        request = self.factory.post('/accounts/django-superstars/', data=self.data_user, format='multipart')
        request.data = self.data_user
        resp = process._create_user(request=request)
        self.assertEqual(resp.username, '79101111111')
        self.assertEqual(resp.status, 'ward')
        self.assertEqual(resp.is_active, False)

        if os.path.exists(f'images/file_user/{file.name}'):
            os.remove(f'images/file_user/{file.name}')

    def test_create_user_philantropist_valid(self):
        """
        Тестирование передачи валидных данных philantropist.
        """
        self.data_user['status'] = 'philantropist'
        request = self.factory.post('/accounts/django-superstars/', data=self.data_user, format='multipart')
        request.data = self.data_user
        resp = process._create_user(request=request)
        self.assertEqual(resp.username, '79101111111')
        self.assertEqual(resp.status, 'philantropist')
        self.assertEqual(resp.is_active, False)

    def test_create_user_email_valid(self):
        """
        Тестирование передачи валидной формы без поля email.
        """
        self.data_user['status'] = 'philantropist'
        del self.data_user['email']
        request = self.factory.post('/accounts/django-superstars/', data=self.data_user, format='multipart')
        request.data = self.data_user
        resp = process._create_user(request=request)
        self.assertEqual(resp.username, '79101111111')
        self.assertEqual(resp.email, '')

    def test_create_user_status_invalid(self):
        """
        Тестирование передачи НЕ валидной формы с отсутствующим статусом.
        """
        self.data_user['status'] = 'ert'
        request = self.factory.post('/accounts/django-superstars/', data=self.data_user, format='multipart')
        request.data = self.data_user
        try:
            process._create_user(request=request)
        except Exception as error:
            self.assertEqual(error.detail['status'][0], 'Значения ert нет среди допустимых вариантов.')

    def test_create_user_ward_invalid(self):
        """
        Тестирование передачи данных ward. НЕ валидная форма.
        Ошибка в связи с отсутствием обязательных для загрузки документов, поле - 'save_file'.
        """
        request = self.factory.post('/accounts/django-superstars/', data=self.data_user, format='multipart')
        request.data = self.data_user

        try:
            process._create_user(request=request)
        except Exception as error:
            self.assertEqual(str(error), 'Необходимо загрузить документы.')


class TestMessageUser(APITestCase):

    def setUp(self):
        self.user_profile = UserData.objects.create_user(
            username='TestUsername',
            phone='TestPhone',
            email='TestEmail',
            status='ward',
            first_name='TestFirst_name',
            last_name='TestLast_name',
            patronymic='TestPatronymic',
            password='TestPassword',
            random_number='123456',
        )

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        file = SimpleUploadedFile('small.gif', small_gif, content_type='image/gif')

        self.file_user = FileUser.objects.create(
            model_file=self.user_profile,
            file_user=file
        )

        self.factory = APIRequestFactory()
        self.request = self.factory.get('/accounts/django-superstars/')
        self.request.user = self.user_profile

        if os.path.exists(f'images/file_user/{file.name}'):
            os.remove(f'images/file_user/{file.name}')

    def test_message_user_flag(self):
        """ Тестирование корректности работы функции message_user флаг == '1' """
        answer = process._message_user(user=self.user_profile, flag=1)
        self.assertEqual(answer, 'Ваш профиль активирован. Войдите в приложение фонда "Скорей добрей"')

    def test_message_user_flag_none(self):
        """ Тестирование корректности работы функции message_user флаг == None """
        answer = process._message_user(user=self.user_profile, flag=None)
        self.assertEqual(self.user_profile.random_number, answer)

    def test_random_int(self):
        """ Тестирование корректности работы функции random_int. Форма вывода - 4 цифры """
        resp = process._random_int()
        self.assertEqual(type(resp), int)
        resp = str(resp)
        self.assertEqual(len(resp), 4)

    def test_get_tokens_for_user(self):
        """ Тест функции выдачи JWT токена """
        resp = process._get_tokens_for_user(user=self.user_profile)
        self.assertEqual(len(resp), 2)
        self.assertEqual(list(resp.keys()), ['refresh', 'access'])

    def test_file_get(self):
        """ Тест функции возвращения списка файлов пользователя """
        resp = process._file_get(request=self.request)
        self.assertEqual(len(resp), 1)

    def test_inf_user_ward(self):
        """ Тест функции возвращение информации о пользователе ward """
        resp = process._inf_user(request=self.request)
        self.assertEqual(resp['phone'], 'TestPhone')
        self.assertEqual(resp['status'], 'ward')
        self.assertEqual(len(resp), 10)

    def test_inf_user_philantropist(self):
        """ Тест функции возвращение информации о пользователе philantropist """
        self.user_profile.status = 'philantropist'
        resp = process._inf_user(request=self.request)
        self.assertEqual(resp['phone'], 'TestPhone')
        self.assertEqual(resp['status'], 'philantropist')
        self.assertEqual(resp['size_donations'], 0)
        self.assertEqual(len(resp), 11)

    def test_file_save(self):
        """ Тест функции массового сохранения файлов """
        file = SimpleUploadedFile("file_test.txt", b"file_content_test")
        file_new = SimpleUploadedFile("file_test_new.txt", b"file_content_test_new")
        resp_post = self.factory.post(
            '/accounts/django-superstars/', data={'save_file': [file, file_new]}, format='multipart'
        )
        resp_post.user = self.user_profile
        resp = process._file_save(request=resp_post)
        self.assertEqual(resp, True)
        file_user = FileUser.objects.filter(model_file=self.user_profile)
        self.assertEqual(file_user.count(), 3)

        if os.path.exists(f'images/file_user/{file.name}'):
            os.remove(f'images/file_user/{file.name}')

        if os.path.exists(f'images/file_user/{file_new.name}'):
            os.remove(f'images/file_user/{file_new.name}')

    def test_save_data_user(self):
        """ Тест функции изменения данных пользователя """
        new_data = {
            'phone': '79101111112',
            'email': 'qwe@mail.ru',
            'first_name': 'TestFirst_name1',
            'last_name': 'TestLast_name1',
            'patronymic': 'TestPatronymic1',
        }

        resp_post = self.factory.post(
            '/accounts/django-superstars/', data=new_data, format='multipart'
        )
        resp_post.user = self.user_profile
        resp_post.data = new_data

        user_form = UserUpdateSerializer(resp_post.user, resp_post.data, partial=True)
        user_form.is_valid(raise_exception=True)
        process._save_data_user(request=resp_post, user_form=user_form)
        resp = UserData.objects.filter(phone='79101111112')
        self.assertEqual(resp.count(), 1)
        self.assertEqual(resp[0].username, '79101111112')
        self.assertEqual(resp[0].first_name, 'TestFirst_name1')
        self.assertEqual(resp[0].last_name, 'TestLast_name1')
        self.assertEqual(resp[0].patronymic, 'TestPatronymic1')

    def test_delete_img(self):
        """ Тест функции удаления файла """
        with open('test.txt', mode='w', encoding='utf-8') as w_file:
            w_file.write('Тестовый файл')
        file_path = [os.path.relpath('test.txt')]
        resp = process._delete_img(url_img=file_path)
        self.assertEqual(resp, True)

    def test_delete_user(self):
        """ Тест функции удаления пользователя """
        user = UserData.objects.filter(phone='TestPhone')
        self.assertEqual(user.count(), 1)
        resp = process._delete_user(request=self.request)
        self.assertEqual(resp, True)
        self.assertEqual(user.count(), 0)

    def test_verification_code(self):
        """
        Тест функции верификации случайного числа, сохраненного в профиле пользователя,
        и числа введенного пользователем. Положительный тест.
        """
        resp = process._verification_code(user=self.user_profile, verification_code=123456)
        self.assertEqual(resp, True)

    def test_verification_code_invalid(self):
        """
        Тест функции верификации случайного числа, сохраненного в профиле пользователя,
        и числа введенного пользователем. Отрицательный тест
        """
        try:
            process._verification_code(user=self.user_profile, verification_code=12345)
        except Exception as error:
            self.assertEqual(str(error), 'Код не совпадает')

    def test_verification_user_ward(self):
        """ Тест функции активации пользователя ward"""
        resp = process._verification_user(user=self.user_profile, verification_code=123456)
        self.assertEqual(resp['message'], 'Дождитесь подтверждения профиля администратором')

    def test_verification_user_philantropist(self):
        """ Тест функции активации пользователя philantropist"""
        self.user_profile.status = 'philantropist'
        self.assertEqual(self.user_profile.is_active, False)
        resp = process._verification_user(user=self.user_profile, verification_code=123456)
        self.assertEqual(list(resp.keys()), ['refresh', 'access'])
        self.assertEqual(self.user_profile.is_active, True)
