from django.urls import path
from doctors import views
from doctors import cedula

urlpatterns = [
    path('listall/', views.RetrieveDoctors),
    path('list/<str:id>/', views.RetrieveDoctor),
    path('update/<str:id>/', views.UpdateDoctor),
    path('create/', views.CreateDoctors),
    path('delete/<str:id>/', views.DeleteDoctor),
    path('CheckCedula/',cedula.CheckCedula),
    path('listspeciality/<str:speciality>/', views.SpecialDoctorList),
    path('createagenda/',views.CreateSchedule),
    path('retrieveagenda/<str:id>/',views.RetriveSchedule),
]