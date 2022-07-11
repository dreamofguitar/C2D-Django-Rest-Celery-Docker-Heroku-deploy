from django.urls import path

from citas import views
      
urlpatterns = [
    path('create/', views.createCitas),
    path('listpat/<str:id_pat>/', views.patListCita),
    path('listcompleted/', views.citaCompletedList),
    path('cancel/<str:id>/', views.cancelCita),
    path('accept/<str:id>/', views.acceptCita),
    path('listdoc/<str:id_doc>/<str:mes>/<str:year>/', views.docListCita),
    path('complete/', views.completeCita),
    path('list/', views.listCitas),
]