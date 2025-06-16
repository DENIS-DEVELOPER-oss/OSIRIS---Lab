from django.contrib import admin
from django.urls import path, include  # necesario para incluir otras apps

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inicio.urls')),  # agregamos la app 'inicio' en la raíz
]