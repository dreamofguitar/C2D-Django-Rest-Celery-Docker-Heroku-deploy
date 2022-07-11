from django.urls import path

from medical_records import views

urlpatterns = [
    path('create/', views.createMedicalRecord),
    path('list/<str:id_pat>/', views.listMedicalRecord),
    path('update/<str:id_pat>/', views.updateMedicalRecord),
    path('delete/<str:id_pat>/', views.deleteMedicalRecord),
]