from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIRequestFactory
from users.models import UserData, FileUser
from users import process


class Test_message_user(APITestCase):

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

        self.file_user=FileUser.objects.create(
            model_file=self.user_profile,
            file_user=file
        )


    def test_message_user_flag(self):
        """ Тестирование корректности работы функции message_user флаг == '1' """
        answer = process._message_user(user=self.user_profile, flag=1)
        self.assertEqual(answer, 'Ваш профиль активирован. Войдите в приложение фонда "Скорей добрей"')


    def test_message_user_flag_none(self):
        """ Тестирование корректности работы функции message_user флаг == None """
        answer = process._message_user(user=self.user_profile, flag=None)
        self.assertEqual(self.user_profile.random_number, answer)


    def test_get_tokens_for_user(self):
        """ Тест функции выдачи JWT токена """
        resp = process._get_tokens_for_user(user=self.user_profile)
        self.assertEqual(len(resp), 2)
        self.assertEqual(list(resp.keys()), ['refresh', 'access'])


    def test_file_get(self):
        """ Тест функции возвращения списка файлов пользователя """
        factory = APIRequestFactory()
        request = factory.get('/accounts/django-superstars/')
        request.user = self.user_profile
        resp = process._file_get(request=request)
        self.assertEqual(len(resp), 1)
