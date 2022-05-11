from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .models import Confectionary
from . import process
from .serializers import ConfectionarySerializer


class RegisterConfectionary(APIView):
    permission_classes= [AllowAny, ]

    def post(self, request, *args, **kwargs):
        if request.user.status == "confectioner":
            user_form = ConfectionarySerializer(request.user, request.data, partial=True)
            user_form.is_valid(raise_exception=True)
            process._confectionary_save(request=request, confectionary_data=user_form.validated_data)

            return JsonResponse({'123': True})

        else:
            return JsonResponse({'error': "You do not have the rights to register a pastry shop"})



