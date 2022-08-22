from django.urls import path
from . import views

app_name = 'business'


urlpatterns = [
    #Order
    path('create_order/', views.CreateOrder.as_view(), name='create_order'),
    path('update_order/', views.UpdateOrder.as_view(), name='update_order'),
    path('payment/', views.PaymentOrder.as_view(), name='payment'),
    path('all_desire_ward/', views.AllDesireWard.as_view(), name='all_desire_ward'),
    path('all_order/', views.AllOrder.as_view(), name='all_order'),
    path('all_order_confectionary/', views.AllOrderConfectionary.as_view(), name='all_order_confectionary'),
    path('execute_an_order/', views.ExecuteAnOrder.as_view(), name='execute_an_order'),

]
