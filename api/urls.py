from django.urls import path

from . import views

urlpatterns = [
    path('getHistoryData/<int:page>/<int:step>/', views.getHistoryData, name='getHistoryData'),
    path('searchRoom/<str:room>/', views.searchRoom, name='searchRoom'),
    path('takeroom_isVar_changed/', views.takeroom_isVar_changed, name='takeroom_isVar_changed'),
    path('get_last5_orders/', views.get_last5_orders, name='get_last5_orders'),
    path('cancel-takeroom/<int:pk>', views.cancel_takeroom, name='cancel-takeroom'),
    path('get-room-schedule/<str:room_number>/', views.get_room_schedule, name='get_room_schedule'),
    path('create-reservation/<str:room_name>/<str:start_time_input>/<int:is_take>/', views.create_reservation, name='create_reservation')
]
