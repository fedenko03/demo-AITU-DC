from django.urls import path

from . import views

urlpatterns = [
    path('st2/', views.takeroom2, name='takeroom2'),
    path('st3/', views.takeroom3, name='takeroom3'),
    path('st4/', views.takeroom4, name='takeroom4'),
    path('final/', views.takeroomFinal, name='takeroomFinal'),
]
