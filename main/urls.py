from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeMain, name='homeMain'),
    path('login/', views.loginMain, name='loginMain'),
    path('logout/', views.logoutMain, name='logoutMain'),
    path('pin/', views.pinLocked, name='pinLocked'),
    path('history/', views.historyMain, name='historyMain'),
    path('history/ajax/', views.history_ajax, name='history_ajax'),
    path('history/export/', views.export_history_to_excel, name='export_history_to_excel'),
    path('users/', views.usersMain, name='usersMain'),
    path('rooms/', views.roomsMain, name='roomsMain'),
    path('settings/', views.settingsMain, name='settingsMain'),
    path('pinlock/<str:code>', views.PinLock, name='PinLock'),
    path('confirm-takeroom/<int:pk>', views.confirm_takeroom, name='confirm-takeroom'),
    path('cancel-takeroomMain/<int:pk>', views.cancel_takeroomMain, name='cancel-takeroomMain'),
   ]
