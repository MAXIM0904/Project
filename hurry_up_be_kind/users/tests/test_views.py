import tempfile
from users.serializers import UserRegistrationSerializer
from django.core.files.uploadedfile import SimpleUploadedFile

# class Test_create_user(APITestCase):
#
#     def test_create_user_ward_invalid(self):
#         """
#         Тестирование передачи данных ward.
#         Ошибка в связи с отсутствием обязательных для загрузки документов.
#         """
#         data_user = {
#                 'username':'TestUsername',
#                 'phone':'79101111111',
#                 'email':'jkljkkl@mail.ru',
#                 'status':'ward',
#                 'first_name':'TestFirst_name',
#                 'last_name':'TestLast_name',
#                 'patronymic':'TestPatronymic',
#                 'password':'TestPassword',
#         }
#
#         print('э890')
#         print(data_user)
#         try:
#             process._create_user(request=data_user)
#         except Exception as error:
#             self.assertEqual(str(error), 'Необходимо загрузить документы.')



    # def test_create_user_ward_invalid(self):
    #     """
    #     Тестирование передачи валидных данных ward.
    #     """
    #
    #
    #     small_gif = (
    #         b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    #         b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
    #         b'\x02\x4c\x01\x00\x3b'
    #     )
    #     file = SimpleUploadedFile("file.txt", b"file_content")
    #
    #
    #     data_user = {
    #         'username':'TestUsername',
    #         'phone':'79101111111',
    #         'email':'jkljkkl@mail.ru',
    #         'status':'ward',
    #         'first_name':'TestFirst_name',
    #         'last_name':'TestLast_name',
    #         'patronymic':'TestPatronymic',
    #         'password':'TestPassword',
    #         'save_file': file
    #     }
    #
    #     serializer = UserRegistrationSerializer(data=data_user)
    #     serializer.is_valid(raise_exception=True)
    #     create_user = process._create_user(serializer_form=serializer)
    #     print(create_user)