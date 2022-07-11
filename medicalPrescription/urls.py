from django.urls import path

from medicalPrescription import views
      
urlpatterns = [
    path('create/', views.createPrescription),
    path('list/', views.listPrescriptions),
    path('listdoc/<str:id_doc>/', views.docListPrescription),
    path('listpat/<str:id_pat>/<str:date>/', views.patListPrescription),
    path('list/<str:id>/', views.listPrescription),
    path('delete/<str:id>/', views.deletePrescription),
]