from django.urls import path

from . import views

urlpatterns = [
    path('form/page-one/', views.form_page_one, name='form_page_one'),
    path('form/page-two/', views.form_page_two, name='form_page_two'),
    path('form/page-success/', views.form_success, name='form_success'),
]
