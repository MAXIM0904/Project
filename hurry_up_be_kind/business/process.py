# from confectionary.models import Confectionary
# from .models import WishesWard
# from users.models import UserData
# from .serializers import InfoWishesWardSerializer
# from menu.models import Menu


# def _order_save(request, order_data):
#     product_id = order_data['product']
#     count_product = order_data['count_product']
#     confectionary = order_data['confectionary']
#     instance = WishesWard.objects.create(
#         ward=request.user,
#         product=product_id,
#         count_product=count_product,
#         confectionary=confectionary,
#     )
#
#     form = InfoWishesWardSerializer(instance)
#     return form
#
#
def _inf_user_data(id_user):
    inf_user = {
        'id': id_user.id,
        'usermane': f"{id_user.first_name} {id_user.last_name}"
    }
    return inf_user


def inf_order(order, status):
    ward = None
    philantropist = None
    confectionary = None
    if order.user_philantropist_id is not None:
        philantropist = _inf_user_data(id_user=order.user_philantropist_id)

    if order.confectionary_id is not None:
        confectionary = {
            'id': order.confectionary_id.id,
            'usermane': order.confectionary_id.confectionary_name,
            'address_ward': order.confectionary_id.address_ward
        }

    if order.user_ward_id is not None:
        ward = _inf_user_data(id_user=order.user_ward_id)

    product = {
        'name_dish': order.product_id.name_dish,
        'section_menu': order.product_id.section_menu,
        'price_dish': float(order.product_id.price_dish),
    }

    instance = {
        'id': order.id,
        'user_philantropist_id': philantropist,
        'confectionary_id': confectionary,
        'user_ward_id': ward,
        'product_id': product,
        'count_menu': order.count_menu,
        'order_status': order.order_status,
        'price_order': float(order.price_order),
        'status_user': status,
    }
    return instance


def status_order(order):
    if order.user_ward_id and order.user_philantropist_id and order.confectionary_id:
        order.order_status = 'formed'
        order.save()
