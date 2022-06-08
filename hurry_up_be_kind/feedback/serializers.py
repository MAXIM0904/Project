from rest_framework import serializers
from .models import Feedback
import datetime

class FeedbackUserSerializer(serializers.ModelSerializer):
    ''' Сериализатор регистрации нового пользователя '''


    class Meta:
        model = Feedback
        fields = ('id', 'phone', 'message_text', 'status', 'registrarion_date')