from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import WishesWard, OrderTaken
from .serializers import WishesWardSerializer, InfoWishesWardSerializer, OrderTakenSerializer, MakeGiftSerializer
from django.http import JsonResponse
from . import process


class WishesWardCreate(APIView):
    ''' Регистрация и получение информации о желании определенного подопечного '''
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if request.user.status == 'ward':
            queryset = WishesWard.objects.filter(ward=request.user)
            instanse_list = []
            for inf_wishes in queryset:
                instance = process._inf_order(instanse_wishes=inf_wishes)
                instanse_list.append(instance)
            return Response(instanse_list)

        return JsonResponse({'registration': 'error',
                             'id': 'Недостаточно прав. Обратитесь к администратору.'})


    def post(self, request):
        if request.user.status == 'ward':
            order_form = WishesWardSerializer(data=request.data)
            order_form.is_valid(raise_exception=True)
            form = process._order_save(request=request, order_data=order_form.validated_data)
            return JsonResponse(form.data)

        return JsonResponse({'registration': 'error',
                             'id': 'Недостаточно прав. Обратитесь к администратору.'})


class AllWishesWard(ListAPIView):
    """ Предоставление всех не взятых желании подопечных """
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = WishesWard.objects.filter(order_wishes='posted')
        instanse_list = []
        for inf_wishes in queryset:
            instance = process._inf_order(instanse_wishes=inf_wishes)
            instanse_list.append(instance)
        return Response(instanse_list)


class DeleteWishesWard(APIView):
    """ Удаление желания подопечного """
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        try:
            instance = WishesWard.objects.get(id=request.data['id_wishes'])
            if request.user.id == instance.ward.id:
                instance.delete()
                return JsonResponse({'status': 'True'})
            else:
                return JsonResponse({'error': 'Доступ запрещен. Обратитесь к администратору.'})

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)})



class OrderTakenUser(APIView):
    """ Класс позволяет взять заказ """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        instance = WishesWard.objects.get(id=request.data['id_wishes'])
        OrderTaken.objects.create(
            user_philantropist_id=request.user,
            wishes_ward_id=instance,
            order_status = 'generated'
        )
        instance.order_wishes = 'taken'
        instance.save()
        return JsonResponse({'status': 'True'})



class MyOrderTaken(ListAPIView):
    """ Класс предоставляет информацию о взятых заказах """
    permission_classes = (IsAuthenticated,)
    queryset = OrderTaken.objects.all()
    serializer_class = OrderTakenSerializer


class OrderPayment(APIView):
    """ Класс оплаты заказа """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        instance = OrderTaken.objects.get(id=request.data['id_order'])
        instance.order_status = 'paid_for'
        instance.save()
        return JsonResponse({'status': 'True'})


class MakeGift(APIView):
    ''' Сделать подарок '''
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        order_form = MakeGiftSerializer(data=request.data)
        order_form.is_valid(raise_exception=True)
        form = order_form.save()
        form.user_philantropist_id = request.user
        form.save()
        instance = MakeGiftSerializer(form)
        return JsonResponse(instance.data)
