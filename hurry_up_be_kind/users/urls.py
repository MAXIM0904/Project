from django.urls import path
from .views import CreateUser, InfUser, UpdateUser, DeleteUser
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('registration_user/', CreateUser.as_view(), name='registration_user'),
    path('inf_user/', InfUser.as_view(), name='inf_user'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('update_user/', UpdateUser.as_view(), name='update_user'),
    path('delete_user/', DeleteUser.as_view(), name='delete_user'),
]
