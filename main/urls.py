from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeMain, name='homeMain'),
   ]
