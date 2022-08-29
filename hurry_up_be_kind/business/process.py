from .models import Order
from menu.models import Menu
from users.models import UserData
from confectionary.models import Confectionary


def repeat_control(instance):
    '''Функция не позволяет сохранять в корзине повторы. При обнаружения обновляет существующую позицию'''
    instance_control = Order.objects.filter(
        user_ward_id=instance.user_ward_id,
        user_philantropist_id=instance.user_philantropist_id,
        confectionary_id=instance.confectionary_id,
        product_id=instance.product_id
    )
    if instance_control:
        instance = instance_control[0]
    return instance


def create_order(request):
    """Функция создания корзины"""
    if request.user.status == 'ward':
        instance = Order(user_ward_id=request.user,
                         order_status='desire_ward'
                         )
    elif request.user.status == 'philantropist':
        instance = Order(user_philantropist_id=request.user)

    else:
        instance = Order(
            user_philantropist_id=request.user,
            confectionary_id=request.user.confectionary
        )
    product = Menu.objects.get(id=request.POST['product_id'])
    instance.product_id = product
    instance = repeat_control(instance)
    instance.price_order = product.price_dish * int(request.POST['count_menu'])
    return instance


def update_order(request):
    """Функция изменения корзины"""
    instance = Order.objects.get(id=request.POST['order_id'])
    if 'user_ward_id' in request.POST:
        instance.user_ward_id = UserData.objects.get(id=request.POST['user_ward_id'])
    if 'user_philantropist_id' in request.POST:
        instance.user_philantropist_id = UserData.objects.get(id=request.POST['user_philantropist_id'])
    if 'confectionary_id' in request.POST:
        instance.confectionary_id = Confectionary.objects.get(id=request.POST['confectionary_id'])
    if instance.user_ward_id and instance.user_philantropist_id and instance.confectionary_id:
        instance.order_status = 'formed'
    if instance.order_status == 'paid_for' and request.status == 'confectioner':
        instance.order_status = 'completed'
    return instance
