from django.urls import path
from .views import FeedbackUser, AllFeedback, ReceivedFeedback, ArchiveFeedback, DeleteFeedback, FeedbackStatus


app_name = 'feedback'


urlpatterns = [
    path('feedback_create/', FeedbackUser.as_view(), name='feedback_create'),
    path('feedback_status/', FeedbackStatus.as_view(), name='feedback_status'),
    path('all_feedback/', AllFeedback.as_view(), name='all_feedback'),
    path('feedback_received/', ReceivedFeedback.as_view(), name='feedback_received'),
    path('feedback_archive/', ArchiveFeedback.as_view(), name='feedback_archive'),
    path('delete_feedback/', DeleteFeedback.as_view(), name='delete_feedback'),
]