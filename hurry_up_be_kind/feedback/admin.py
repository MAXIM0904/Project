from django.contrib import admin
from .models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['phone', 'message_text', 'status', 'registrarion_date']
    search_fields = ('status', 'registrarion_date')


admin.site.register(Feedback, FeedbackAdmin)
