from django.urls import path

from . import views

app_name = 'productores'

urlpatterns = [
    path('', views.modulo, name='modulo'),
]
