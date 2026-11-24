from django.urls import path

from . import views

app_name = 'comercializacion'

urlpatterns = [
    path('', views.modulo, name='modulo'),
]
