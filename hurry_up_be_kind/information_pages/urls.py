from django.urls import path
from .views import privacy_policy, personal_data


app_name = 'information_pages'

urlpatterns = [
    path('privacy_policy/', privacy_policy, name='privacy_policy'),
    path('personal_data/', personal_data, name='personal_data'),
]