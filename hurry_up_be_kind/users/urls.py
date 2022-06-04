from django.urls import path
from .views import RegistrationUser, InfUser, UpdateUser, DeleteUser, AllUsers, home_page, Verification_sms
from .views import AllPhilantropist, AllWard

urlpatterns = [
    path('', home_page, name='home_page'),
    path('registration_user/', RegistrationUser.as_view(), name='registration_user'),
    path('inf_user/', InfUser.as_view(), name='inf_user'),
    path('update_user/', UpdateUser.as_view(), name='update_user'),
    path('delete_user/', DeleteUser.as_view(), name='delete_user'),
    path('all_user/', AllUsers.as_view(), name='all_user'),
    path('all_ward/', AllWard.as_view(), name='all_ward'),
    path('all_philantropist/', AllPhilantropist.as_view(), name='all_philantropist'),
    path('verification_sms/', Verification_sms.as_view(), name='verification_sms')
]
