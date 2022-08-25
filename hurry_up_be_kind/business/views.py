from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from .serializers import OrderSerializer
from django.http import JsonResponse
from . import process
from menu.models import Menu


class CreateOrder(APIView):
    """Класс добавления в корзину"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.status == 'ward':
            instanse = Order(user_ward_id=request.user,
                             order_status='desire_ward'
                             )
        elif request.user.status == 'philantropist':
            instanse = Order(user_philantropist_id=request.user)
        elif request.user.status == 'confectioner':
            instanse = Order(
                user_philantropist_id=request.user,
                confectionary_id=request.user.confectionary
            )

        product = Menu.objects.get(id=request.POST['product_id'])

        instanse.product_id = product
        instanse.count_menu = int(request.POST['count_menu'])
        instanse.price_order = product.price_dish * instanse.count_menu
        instanse_control = Order.objects.filter(
                user_ward_id=instanse.user_ward_id,
                user_philantropist_id=instanse.user_philantropist_id,
                confectionary_id=instanse.confectionary_id,
                count_menu=instanse.count_menu,
                product_id = instanse.product_id
        )

        if instanse_control:
            instanse = instanse_control[0]
        else:
            instanse.save()

        order = process.inf_order(order=instanse, status=request.user.status)
        return JsonResponse(order, json_dumps_params={'ensure_ascii': False})


class UpdateOrder(APIView):
    """Класс изменения корзины"""
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        model_object = Order.objects.get(id=request.POST['order_id'])
        print(request.POST)
        if 'user_philantropist_id' in list(request.POST):
            if request.POST['user_philantropist_id']:
                model_object.user_philantropist_id = request.user
                model_object.save()
        else:
            serializer = OrderSerializer(model_object, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        process.status_order(order=model_object)
        order = process.inf_order(order=model_object, status=request.user.status)
        return JsonResponse(order, json_dumps_params={'ensure_ascii': False})


class PaymentOrder(APIView):
    """Оплата заказа"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        instanse_order = Order.objects.get(id=request.POST['order_id'])
        instanse_order.order_status = 'paid_for'
        instanse_order.save()
        order = process.inf_order(order=instanse_order, status=request.user.status)
        return JsonResponse(order, json_dumps_params={'ensure_ascii': False})


class AllOrder(ListAPIView):
    """Все заказы пользователя"""
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if request.user.status in 'ward':
            queryset = Order.objects.filter(user_ward_id=request.user)
        if request.user.status in ['philantropist', 'confectioner']:
            queryset = Order.objects.filter(user_philantropist_id=request.user)

        instanse_list = []

        for inf_wishes in queryset:
            instance = process.inf_order(order=inf_wishes, status=request.user.status)
            instanse_list.append(instance)

        return JsonResponse(instanse_list, safe=False)


class AllOrderConfectionary(ListAPIView):
    """Все заказы для кондитерской"""
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        if request.user.status in 'confectioner':
            queryset = Order.objects.filter(confectionary_id=request.user.confectionary, order_status='paid_for')
            instanse_list = []
            for inf_wishes in queryset:
                instance = process.inf_order(order=inf_wishes, status=request.user.status)
                instanse_list.append(instance)

            return JsonResponse(instanse_list, safe=False)


class ExecuteAnOrder(APIView):
    """Все заказы для кондитерской"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        instanse_order = Order.objects.get(id=request.POST['order_id'])
        instanse_order.order_status = 'completed'
        instanse_order.save()
        return JsonResponse({'status': "True"})


class AllDesireWard(ListAPIView):
    """ Класс предоставляет данные о желании подопечных """
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(order_status="desire_ward")
        instanse_list = []
        print('7897879')
        for inf_wishes in queryset:
            instance = process.inf_order(order=inf_wishes, status=request.user.status)
            instanse_list.append(instance)

        return JsonResponse(instanse_list, safe=False)
