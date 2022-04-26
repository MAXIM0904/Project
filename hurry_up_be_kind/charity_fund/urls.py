from django.urls import path
from .views import list_news

urlpatterns = [
    path('', list_news, name='list_news'),
]