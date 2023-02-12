from django.urls import path

from . import views

urlpatterns = [
    path('', views.homeMain, name='homeMain'),
    path('login/', views.loginMain, name='loginMain'),
    path('logout/', views.logoutMain, name='logoutMain'),
    path('pin/', views.pinLocked, name='pinLocked'),
    path('history/', views.historyMain, name='historyMain'),
    path('users/', views.usersMain, name='usersMain'),
    path('rooms/', views.roomsMain, name='roomsMain'),
    path('confirm-takeroom/<int:pk>', views.confirm_takeroom, name='confirm-takeroom'),
    path('cancel-takeroom/<int:pk>', views.cancel_takeroom, name='cancel-takeroom'),
    path('cancel-takeroomMain/<int:pk>', views.cancel_takeroomMain, name='cancel-takeroomMain'),
   ]
