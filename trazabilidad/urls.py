from django.urls import path

from . import views

app_name = 'trazabilidad'

urlpatterns = [
    path('', views.modulo, name='modulo'),
]
