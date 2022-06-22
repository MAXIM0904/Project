from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import WishesWard
from .serializers import WishesWardSerializer, InfoWishesWardSerializer
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
    '''Предоставление всех пожелания в базе данных '''
    permission_classes = (IsAuthenticated,)
    queryset = WishesWard.objects.all()


    def list(self, request, *args, **kwargs):
        queryset = WishesWard.objects.all()
        instanse_list = []
        for inf_wishes in queryset:
            instance = process._inf_order(instanse_wishes=inf_wishes)
            instanse_list.append(instance)
        return Response(instanse_list)


class DeleteWishesWard(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        print(request.data['id_wishes'])
        try:
            print(request)
            instance = WishesWard.objects.get(id=request.data['id_wishes'])
            if request.user.id == instance.ward.id:
                instance.delete()
                return JsonResponse({'status': 'True'})
            else:
                return JsonResponse({'error': 'Доступ запрещен. Обратитесь к администратору.'})

        except Exception as error:
            return JsonResponse({'registration': 'error',
                                 'id': str(error)})




# class MyWishesWard(ListAPIView):
#     '''Предоставление пожеланий конкретного пользователя '''
#     permission_classes = (IsAuthenticated,)
#     queryset = WishesWard.objects.filter(id=request.id)
#
#     def list(self, request, *args, **kwargs):
#         queryset = WishesWard.objects.all()
#         instanse_list = []
#         for inf_wishes in queryset:
#             instance = process._inf_order(instanse_wishes=inf_wishes)
#             instanse_list.append(instance)
#         return Response(instanse_list)