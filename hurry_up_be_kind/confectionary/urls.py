from django.urls import path
from .views import RegisterConfectionary, AllConfectionary, UpdateConfectionary, DeleteConfectionary, InfConfectionary

app_name = 'confectionary'

urlpatterns = [
    path('register_confectionary/', RegisterConfectionary.as_view(), name='register_confectionary'),
    path('all_confectionary/', AllConfectionary.as_view(), name='all_confectionary'),
    path('update_confectionary/', UpdateConfectionary.as_view(), name='update_confectionary'),
    path('delete_confectionary/', DeleteConfectionary.as_view(), name='delete_confectionary'),
    path('inf_confectionary/', InfConfectionary.as_view(), name='inf_confectionary'),
]