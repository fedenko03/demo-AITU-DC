from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeMain, name='homeMain'),
    path('404/', views.not_foundMain, name='not_foundMain'),
    path('login/', views.loginMain, name='loginMain'),
    path('logout/', views.logoutMain, name='logoutMain'),
    path('pin/', views.pinLocked, name='pinLocked'),
    path('history/', views.historyMain, name='historyMain'),
    path('history/ajax/', views.history_ajax, name='history_ajax'),
    path('history/export/', views.export_history_to_excel, name='export_history_to_excel'),
    path('users/', views.usersMain, name='usersMain'),
    path('rooms/', views.roomsMain, name='roomsMain'),
    path('get_room_map/', views.get_room_map, name='get_room_map'),
    path('get_rooms_floor/', views.get_rooms_floor, name='get_rooms_floor'),
    path('settings/', views.settingsMain, name='settingsMain'),
    path('pinlock/<str:code>', views.PinLock, name='PinLock'),
    path('confirm-takeroom/<int:pk>', views.confirm_takeroom, name='confirm-takeroom'),
    path('cancel-takeroomMain/<int:pk>', views.cancel_takeroomMain, name='cancel-takeroomMain'),
    path('confirm-booking/<str:key>/', views.confirmBooking, name='confirm-booking'),
    path('qr/', views.websocketQR, name='websocketQR'),
    path('update-qr/', views.updateQR, name='updateQR'),
    path('schedule/', views.schedule_page, name='schedule_page')
   ]
