from django.urls import path

from citas_express import views 

urlpatterns = [
    path('create/', views.createCitaExp),
    path('check/<str:id>/', views.checkCita),
    path('waiting-room/', views.waitingRoom),
    path('takecita/<str:id>/', views.takeCita),
    path('complete/<str:id>/', views.completeCitaExp),
]