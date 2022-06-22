from .models import Order, WishesWard
from .serializers import InfoWishesWardSerializer


def _status_ward(request, order_data):
    print(order_data)
    #
    # Order.objects.create(
    #     confectionary_id=order_data['confectionary_id'],
    #     user_ward_id=request.user,
    #     product_id=order_data['product_id'],
    #     order_status='admitted',
    # )

    #
    #
    # if status == 'confectioner':
    #     Order.objects.create(
    #         confectionary_id=request.user.confectionary,
    #         user_philantropist_id=request.user,
    #         product_id=order_data['product_id'],
    #         order_status='admitted',
    #     )
    # elif status == 'ward':
    #     Order.objects.create(
    #         confectionary_id=order_data['confectionary_id'],
    #         user_ward_id=request.user,
    #         product_id=order_data['product_id'],
    #         order_status='admitted',
    #     )
    # elif status == 'philantropist':
    #     print('2')
    #     print(order_data['confectionary_id'])
    #     Order.objects.create(
    #         confectionary_id=order_data['confectionary_id'],
    #         product_id=order_data['product_id'],
    #         user_philantropist_id=request.user,
    #         order_status='admitted',
    #     )
    # else:
    #     raise ValueError('Пользователя с таким id не существует')
    return True

def _order_save(request, order_data):
    product_id = order_data['product']
    count_product = order_data['count_product']
    confectionary = order_data['confectionary']
    instance = WishesWard.objects.create(
        ward=request.user,
        product=product_id,
        count_product=count_product,
        confectionary=confectionary,
        order_status='generated',
    )
    form = InfoWishesWardSerializer(instance)
    return form


def _inf_order(instanse_wishes):
    price_dish = instanse_wishes.product.price_dish
    count_product = instanse_wishes.count_product
    total_price = price_dish * count_product
    instance = {
        'id': instanse_wishes.id,
        'ward': {
            'phone': instanse_wishes.ward.phone,
            'first_name': instanse_wishes.ward.first_name,
            'last_name': instanse_wishes.ward.last_name,
        },
        'confectionary': {
            'confectionary_name': instanse_wishes.confectionary.confectionary_name,
            'number_phone': instanse_wishes.confectionary.number_phone,
            'address_ward': instanse_wishes.confectionary.address_ward,
            'description_confectionary': instanse_wishes.confectionary.description_confectionary,
        },
        'count_product': count_product,
        'order_status': instanse_wishes.order_status,
        'product': {'name_dish': instanse_wishes.product.name_dish,
                    'price_dish': price_dish,
                    'weight_dish': instanse_wishes.product.weight_dish,
                    'description_dish': instanse_wishes.product.description_dish,
                    'composition_dish': instanse_wishes.product.composition_dish,
                    'total_price': total_price,
                    },
    }
    return instance