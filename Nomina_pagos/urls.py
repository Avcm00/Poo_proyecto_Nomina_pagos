from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('index/', views.index, name="index"),
    
    # URLs dinámicas para interactuar con cualquier modelo
    path('modelo/<str:modelo>/', views.listar_modelo, name="listar_modelo"),
    path('modelo/<str:modelo>/detalle/<int:id>/', views.detalle_modelo, name="detalle_modelo"),
    path('modelo/<str:modelo>/nuevo/', views.formulario_modelo, name="nuevo_modelo"),
    path('modelo/<str:modelo>/editar/<int:id>/', views.formulario_modelo, name="editar_modelo"),
    path('modelo/<str:modelo>/eliminacion/<int:id>/', views.formulario_modelo, name="eliminacion"),
]