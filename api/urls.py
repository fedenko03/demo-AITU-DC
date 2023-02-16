from django.urls import path

from . import views

urlpatterns = [
    path('getHistoryData/<int:page>/<int:step>/', views.getHistoryData, name='getHistoryData'),
    path('searchRoom/<str:room>/', views.searchRoom, name='searchRoom'),
    path('takeroom_isVar_changed/', views.takeroom_isVar_changed, name='takeroom_isVar_changed'),
    path('get_last5_orders/', views.get_last5_orders, name='get_last5_orders'),
    path('cancel-takeroom/<int:pk>', views.cancel_takeroom, name='cancel-takeroom'),
]
