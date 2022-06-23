from django.urls import path
from .views import WishesWardCreate, AllWishesWard, DeleteWishesWard, OrderTakenUser, MyOrderTaken, OrderPayment, \
    MakeGift

app_name = 'business'


urlpatterns = [
    path('wishes_ward_create/', WishesWardCreate.as_view(), name='wishes_ward_create'),
    path('all_wishes_ward/', AllWishesWard.as_view(), name='all_wishes_ward'),
    path('delete_wishes_ward/', DeleteWishesWard.as_view(), name='delete_wishes_ward'),
    path('order_taken/', OrderTakenUser.as_view(), name='order_taken'),
    path('my_order_taken/', MyOrderTaken.as_view(), name='my_order_taken'),
    path('order_payment/', OrderPayment.as_view(), name='order_payment'),
    path('make_gift/', MakeGift.as_view(), name='make_gift'),
]