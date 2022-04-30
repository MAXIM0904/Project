from django.urls import path
from .views import list_news

app_name = 'business'



urlpatterns = [
    path('', list_news, name='list_news'),
]