from django.urls import path
from .views import RegistrationUser, InfUser, UpdateUser, DeleteUser, AllUsers, home_page

urlpatterns = [
    path('', home_page, name='home_page'),
    path('registration_user/', RegistrationUser.as_view(), name='registration_user'),
    path('inf_user/', InfUser.as_view(), name='inf_user'),
    path('update_user/', UpdateUser.as_view(), name='update_user'),
    path('delete_user/', DeleteUser.as_view(), name='delete_user'),
    path('all_user/', AllUsers.as_view(), name='all_user'),
]
