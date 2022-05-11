from django.urls import path
from .views import RegisterConfectionary

app_name = 'confectionary'

urlpatterns = [
    path('register_confectionary/', RegisterConfectionary.as_view(), name='register_confectionary'),
]