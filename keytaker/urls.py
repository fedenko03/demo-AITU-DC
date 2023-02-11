from django.urls import path

from . import views

urlpatterns = [
    path('st2/', views.takeroom2, name='takeroom2'),
    path('st3/', views.takeroom3, name='takeroom3'),
    path('st4/', views.takeroom4, name='takeroom4'),
    path('final/', views.takeroomFinal, name='takeroomFinal'),
    path('takeroom_isVar_changed/', views.takeroom_isVar_changed, name='takeroom_isVar_changed'),
    path('get_last5_orders/', views.get_last5_orders, name='get_last5_orders'),
]
