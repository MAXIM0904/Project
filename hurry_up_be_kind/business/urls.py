from django.urls import path
from .views import WishesWardCreate, AllWishesWard, DeleteWishesWard

app_name = 'business'


urlpatterns = [
    path('wishes_ward_create/', WishesWardCreate.as_view(), name='wishes_ward_create'),
    path('all_wishes_ward/', AllWishesWard.as_view(), name='all_wishes_ward'),
    path('delete_wishes_ward/', DeleteWishesWard.as_view(), name='delete_wishes_ward'),
]