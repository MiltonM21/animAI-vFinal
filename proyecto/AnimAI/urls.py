from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('registrarme.html', views.registrarme, name='registrarme'),
    path('index.html', views.index, name='index'),
    path('inicio.html', views.inicio, name='inicio'),
    path('configuracion.html', views.configuracion, name='configuracion'),
    path('cuenta.html', views.cuenta, name='cuenta'),
    path('historial.html', views.historial, name='historial'),
    path('img.html',views.img,name='img'),    
]
