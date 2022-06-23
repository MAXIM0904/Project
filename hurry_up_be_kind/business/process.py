from .models import WishesWard
from .serializers import InfoWishesWardSerializer


def _order_save(request, order_data):
    product_id = order_data['product']
    count_product = order_data['count_product']
    confectionary = order_data['confectionary']
    instance = WishesWard.objects.create(
        ward=request.user,
        product=product_id,
        count_product=count_product,
        confectionary=confectionary,
    )

    form = InfoWishesWardSerializer(instance)
    return form


def _inf_order(instanse_wishes):
    price_dish = instanse_wishes.product.price_dish
    count_product = instanse_wishes.count_product
    total_price = price_dish * count_product
    instance = {
        'id': instanse_wishes.id,
        'order_wishes': instanse_wishes.order_wishes,
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
        'product': {'name_dish': instanse_wishes.product.name_dish,
                    'price_dish': price_dish,
                    'weight_dish': instanse_wishes.product.weight_dish,
                    'description_dish': instanse_wishes.product.description_dish,
                    'composition_dish': instanse_wishes.product.composition_dish,
                    'total_price': total_price,
                    },
    }
    return instance