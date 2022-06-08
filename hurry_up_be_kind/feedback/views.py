from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.views import APIView
from . import process
from .models import Feedback
from .serializers import FeedbackUserSerializer


class FeedbackUser(CreateAPIView):
    """Функция регистрации сообщений обратной связи"""
    permission_classes = (AllowAny,)
    serializer_class = FeedbackUserSerializer


class FeedbackStatus(APIView):
    permission_classes = (IsAdminUser,)

    def post(self, request):
        instance_feedback = Feedback.objects.get(id=request.POST['id'])
        process._update_status(instance_feedback=instance_feedback)
        message_feedback = FeedbackUserSerializer(instance_feedback)
        return JsonResponse(message_feedback.data)


class AllFeedback(ListAPIView):
    """Предоставление всех сообщений обратной связи"""
    permission_classes = (IsAdminUser,)
    queryset = Feedback.objects.all()
    serializer_class = FeedbackUserSerializer


class ReceivedFeedback(ListAPIView):
    """Предоставление активных сообщений обратной связи"""
    permission_classes = (IsAdminUser,)
    queryset = Feedback.objects.filter(status="received")
    serializer_class = FeedbackUserSerializer


class ArchiveFeedback(ListAPIView):
    """Предоставление архивных сообщений обратной связи"""
    permission_classes = (IsAdminUser,)
    queryset = Feedback.objects.filter(status="archive")
    serializer_class = FeedbackUserSerializer


class DeleteFeedback(DestroyAPIView):
    """Класс удаления сообщений обратной связи"""
    permission_classes = (IsAdminUser,)

    def delete(self, request, *args, **kwargs):
        instance = Feedback.objects.get(id=request.POST['id'])
        instance.delete()
        return JsonResponse({'delete': 'True'})