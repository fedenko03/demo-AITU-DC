from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('404/', views.not_foundUser, name='not_foundUser'),
    path('confirm_registration/', views.confirm_registration, name='confirm_registration'),
    path('confirm_keytaking/token=<confirmation_code>', views.confirm_keytaking, name='confirm_keytaking'),
    path('key_return_get_user/token=<token>', views.key_return_get_user, name='key_return_get_user'),
    path('', views.home, name='home'),
    path('history/', views.history_user, name='history_user'),
    path('settings/', views.settings_user, name='settings_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    path('reserve-studyroom/<str:key>/', views.reserve_studyroom, name='reserve_studyroom'),
]
