from django.urls import path
from . import views
urlpatterns = [
    path('token/', views.token),
    path('save/',views.save_twtest_token),
    path('test_token/',views.retrieve_twtest_token),
    path('all_test_token/',views.retrieve_all_twtest_token),
]