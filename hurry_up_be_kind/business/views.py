from rest_framework.generics import ListAPIView, UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Order
from .serializers import OrderSerializer
from django.http import JsonResponse
from . import process


class CreateOrder(CreateAPIView):
    """Класс добавления в корзину"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        instance = process.create_order(request)
        serializer = OrderSerializer(instance, data=request.POST, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=False)


class UpdateOrder(APIView):
    """ Класс изменения корзины """
    permission_classes = (IsAuthenticated,)

    def patch(self, request):
        instance = process.update_order(request)
        serializer = OrderSerializer(instance, data=request.POST, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, safe=False)


class AllOrder(ListAPIView):
    """Заказы пользователя за исключением оплаченных"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        if request.user.status in 'ward':
            queryset = Order.objects.filter(user_ward_id=request.user).exclude(order_status='paid_for')
        if request.user.status in ['philantropist', 'confectioner']:
            queryset = Order.objects.filter(user_philantropist_id=request.user).exclude(order_status='paid_for')
        serializer = OrderSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)


class PaymentOrder(APIView):
    """Оплата заказа"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        instance = Order.objects.get(id=request.POST['order_id'])
        instance.order_status = 'paid_for'
        serializer = OrderSerializer(instance, data=request.POST, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.save()
        return JsonResponse(serializer.data, safe=False)


class ExecuteAnOrder(APIView):
    """Исполнение заказа кондитерской"""
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        print('89080980')
        instance = process.update_order(request)
        instance.save()
        serializer = OrderSerializer(instance)
        return JsonResponse(serializer.data, safe=False)


class AllOrderConfectionary(ListAPIView):
    """Все заказы для кондитерской"""
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        if request.user.status in 'confectioner':
            queryset = Order.objects.filter(confectionary_id=request.user.confectionary, order_status='paid_for')
            instanse_list = []
            for inf_wishes in queryset:
                serializer = OrderSerializer(inf_wishes)
                instanse_list.append(serializer.data)
            return JsonResponse(instanse_list, safe=False)
        else:
            return JsonResponse({
                "registration": "error",
                "id": "Нет прав доступа"
            })


class AllDesireWard(ListAPIView):
    """ Класс предоставляет данные о желании всех подопечных """
    permission_classes = (IsAuthenticated,)
    queryset = Order.objects.filter(order_status="desire_ward")
    serializer_class = OrderSerializer
