from django.urls import path

from . import views

urlpatterns = [
    path('step2/', views.step2, name='step2'),
    path('success/', views.success, name='success')
]
