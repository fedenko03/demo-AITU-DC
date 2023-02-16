from django.urls import path

from . import views

urlpatterns = [
    path('', views.keyreturnerMain, name='keyreturnerMain'),
    path('returnKeyConfirm/<int:id>/', views.returnKeyConfirm, name='returnKeyConfirm'),
]
