from django.urls import path

from patients import views

urlpatterns = [
    path('create/', views.patientCreate, name='Create Patient'),
    path('listall/', views.listAll, name='List Patients'),
    path('list/<str:id>/', views.listPatient, name='List a Patient'),
    path('update/<str:id>/', views.patientUpdate, name='Update a Patient'),
    path('delete/<str:pk>/', views.patientDelete, name='Delete a Patient'),

]