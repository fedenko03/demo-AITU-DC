from django.urls import path

from . import views

urlpatterns = [
    path('', views.keyreturnerMain, name='keyreturnerMain'),
    path('getHistoryData/<int:page>/<int:step>/', views.getHistoryData, name='getHistoryData'),
    path('returnKeyConfirm/<int:id>/', views.returnKeyConfirm, name='returnKeyConfirm'),
    path('searchRoom/<str:room>/', views.searchRoom, name='searchRoom'),
]
