from django.urls import path
from users.views import users 

urlpatterns = [
    path('register/', users.register),
    path('token/', users.token),
    path('token/refresh/', users.refresh_token),
    path('token/revoke/', users.revoke_token),
    path('emailverify/',users.emailverification),
]