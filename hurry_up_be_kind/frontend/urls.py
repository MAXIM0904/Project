from django.urls import path, re_path
from . import views

app_name = 'hurry_up_be_kind'


urlpatterns = [
    #user
    path('index/', views.index, name='index'),
    path('registration/', views.registration, name='registration'),
    path('sms_confirmation/', views.sms_confirmation, name='sms_confirmation'),
    path('getting_your_data/', views.getting_your_data, name='getting_your_data'),
    path('changing_data/', views.changing_data, name='changing_data'),
    path('logging_user/', views.logging_user, name='logging_user'),
    #confectionary
    path('registration_confectionary/', views.registration_confectionary, name='registration_confectionary'),
    path('pastry_shop_office/', views.pastry_shop_office, name='pastry_shop_office'),
    path('update_confectionary/', views.update_confectionary, name='update_confectionary'),
    #menu
    path('bulk_loading_menu/', views.bulk_loading_menu, name='bulk_loading_menu'),
    re_path('menu_list/[^\s]*', views.menu_list, name='menu_list'),

]