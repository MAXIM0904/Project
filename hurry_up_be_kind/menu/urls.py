from django.urls import path
from .views import RegisterMenu, AllEconomyMenu, AllBusinessMenu, AllOptimalMenu, MassiveMenuUpdate


app_name = 'menu'


urlpatterns = [
    path('register_menu/', RegisterMenu.as_view(), name='register_menu'),
    path('all_economy_menu/', AllEconomyMenu.as_view(), name='all_economy_menu'),
    path('all_optimal_menu/', AllOptimalMenu.as_view(), name='all_optimal_menu'),
    path('all_business_menu/', AllBusinessMenu.as_view(), name='all_business_menu'),
    path('massive_menu_update/', MassiveMenuUpdate.as_view(), name='massive_menu_update'),
]