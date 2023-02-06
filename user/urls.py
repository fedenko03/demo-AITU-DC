from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('confirm_registration/', views.confirm_registration, name='confirm_registration'),
    path('confirm_keytaking/token=<confirmation_code>', views.confirm_keytaking, name='confirm_keytaking'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
]
