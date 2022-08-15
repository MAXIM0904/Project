from django.urls import path
from . import views

app_name = 'business'


urlpatterns = [
    # path('wishes_ward_create/', views.WishesWardCreate.as_view(), name='wishes_ward_create'),
    # path('all_wishes_ward/', views.AllWishesWard.as_view(), name='all_wishes_ward'),
    # path('delete_wishes_ward/', views.DeleteWishesWard.as_view(), name='delete_wishes_ward'),
    # path('order_taken/', views.OrderTakenUser.as_view(), name='order_taken'),
    # path('my_order_taken/', views.MyOrderTaken.as_view(), name='my_order_taken'),
    # path('order_payment/', views.OrderPayment.as_view(), name='order_payment'),
    # path('make_gift/', views.MakeGift.as_view(), name='make_gift'),
    #Order
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    path('all_desire_ward/', views.AllDesireWard.as_view(), name='all_desire_ward'),
    path('update_order/', views.UpdateOrder.as_view(), name='update_order'),
    path('payment/', views.PaymentOrder.as_view(), name='payment'),
    path('all_order/', views.AllOrder.as_view(), name='all_order'),
    path('all_order_confectionary/', views.AllOrderConfectionary.as_view(), name='all_order_confectionary'),
    path('execute_an_order/', views.ExecuteAnOrder.as_view(), name='execute_an_order'),
]
