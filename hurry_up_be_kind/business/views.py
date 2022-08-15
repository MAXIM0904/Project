# from rest_framework.response import Response
from requests import Response
from rest_framework.generics import ListAPIView #, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated #, AllowAny
from .models import Order, OrderExecution  # WishesWard, OrderTaken
from .serializers import OrderSerializer, \
    OrderExecutionSerializer  # WishesWardSerializer, OrderTakenSerializer,  MakeGiftSerializer
from django.http import JsonResponse
from django.shortcuts import redirect
from . import process
from menu.models import Menu


# class WishesWardCreate(APIView):
#     ''' Регистрация и получение информации о желании определенного подопечного '''
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         if request.user.status == 'ward':
#             queryset = WishesWard.objects.filter(ward=request.user)
#             instanse_list = []
#             for inf_wishes in queryset:
#                 instance = process._inf_order(instanse_wishes=inf_wishes)
#                 instanse_list.append(instance)
#             return Response(instanse_list)
#
#         return JsonResponse({'registration': 'error',
#                              'id': 'Недостаточно прав. Обратитесь к администратору.'})
#
#
#     def post(self, request):
#         if request.user.status == 'ward':
#             order_form = WishesWardSerializer(data=request.data)
#             order_form.is_valid(raise_exception=True)
#             form = process._order_save(request=request, order_data=order_form.validated_data)
#             return JsonResponse(form.data)
#
#         return JsonResponse({'registration': 'error',
#                              'id': 'Недостаточно прав. Обратитесь к администратору.'})
#
#
# class AllWishesWard(ListAPIView):
#     """ Предоставление всех не взятых желании подопечных """
#     permission_classes = (IsAuthenticated,)
#
#     def list(self, request, *args, **kwargs):
#         queryset = WishesWard.objects.filter(order_wishes='posted')
#         instanse_list = []
#         for inf_wishes in queryset:
#             instance = process._inf_order(instanse_wishes=inf_wishes)
#             instanse_list.append(instance)
#         return Response(instanse_list)
#
#
# class DeleteWishesWard(APIView):
#     """ Удаление желания подопечного """
#     permission_classes = (IsAuthenticated,)
#
#     def delete(self, request):
#         try:
#             instance = WishesWard.objects.get(id=request.data['id_wishes'])
#             if request.user.id == instance.ward.id:
#                 instance.delete()
#                 return JsonResponse({'status': 'True'})
#             else:
#                 return JsonResponse({'error': 'Доступ запрещен. Обратитесь к администратору.'})
#
#         except Exception as error:
#             return JsonResponse({'registration': 'error',
#                                  'id': str(error)})
#
#
#
# class OrderTakenUser(APIView):
#     """ Класс позволяет взять заказ """
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         instance = WishesWard.objects.get(id=request.data['id_wishes'])
#         OrderTaken.objects.create(
#             user_philantropist_id=request.user,
#             wishes_ward_id=instance,
#             order_status = 'generated'
#         )
#         instance.order_wishes = 'taken'
#         instance.save()
#         return JsonResponse({'status': 'True'})
#
#
#
# class MyOrderTaken(ListAPIView):
#     """ Класс предоставляет информацию о взятых заказах """
#     permission_classes = (IsAuthenticated,)
#     queryset = OrderTaken.objects.all()
#     serializer_class = OrderTakenSerializer
#
#
# class OrderPayment(APIView):
#     """ Класс оплаты заказа """
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         instance = OrderTaken.objects.get(id=request.data['id_order'])
#         instance.order_status = 'paid_for'
#         instance.save()
#         return JsonResponse({'status': 'True'})
#
#
# class MakeGift(APIView):
#     ''' Сделать подарок '''
#     permission_classes = (IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#         order_form = MakeGiftSerializer(data=request.data)
#         order_form.is_valid(raise_exception=True)
#         form = order_form.save()
#         form.user_philantropist_id = request.user
#         form.save()
#         instance = MakeGiftSerializer(form)
#         return JsonResponse(instance.data)
#
# class AllOrder(ListAPIView):
#     """ Класс предоставляет данные о желании подопечных """
#     permission_classes = (IsAuthenticated,)
#
#     def list(self, request, *args, **kwargs):
#         queryset = Order.objects.filter(order_status="desire_ward")
#         instanse_list = []
#         for inf_wishes in queryset:
#             instance = process.inf_order(order=inf_wishes)
#             instanse_list.append(instance)
#         return JsonResponse(instanse_list, json_dumps_params={'ensure_ascii': False})

class AllDesireWard(ListAPIView):
    """ Класс предоставляет данные о желании подопечных """
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = Order.objects.filter(order_status="desire_ward")
        instanse_list = []
        for inf_wishes in queryset:
            instance = process.inf_order(order=inf_wishes)
            instanse_list.append(instance)
        return JsonResponse(instanse_list, json_dumps_params={'ensure_ascii': False})


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

    def patch(self, request, *args, **kwargs):
        model_object = Order.objects.get(id=request.POST['order_id'])
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
        # if request.user.status in 'confectioner':
        #     queryset = Order.objects.filter(confectionary_id=request.user.confectionary)

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
        print('8897887887978')
        print(request.POST)
        instanse_order = Order.objects.get(id=request.POST['order_id'])
        instanse_order.order_status = 'completed'
        instanse_order.save()
        return JsonResponse({'status': "True"})
