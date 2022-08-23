from django.contrib.auth.views import PasswordChangeView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('registration_user/', views.RegistrationUser.as_view(), name='registration_user'),
    path('inf_user/', views.InfUser.as_view(), name='inf_user'),
    path('update_user/', views.UpdateUser.as_view(), name='update_user'),
    path('delete_user/', views.DeleteUser.as_view(), name='delete_user'),
    path('all_user/', views.AllUsers.as_view(), name='all_user'),
    path('all_ward/', views.AllWard.as_view(), name='all_ward'),
    path('all_philantropist/', views.AllPhilantropist.as_view(), name='all_philantropist'),
    path('verification_sms/', views.VerificationSms.as_view(), name='verification_sms'),
    path('password_recovery/', views.PasswordRecovery.as_view(), name='password_recovery'),
    path('password_replacement/', views.PasswordReplacement.as_view(), name='password_replacement'),
]
