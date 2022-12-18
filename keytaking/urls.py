from django.urls import path

from . import views

urlpatterns = [
    path('step2/', views.step2, name='step2'),
    path('step3/', views.step3, name='step3'),
    path('step4/', views.step4, name='step4'),
    path('success/', views.success, name='success')
]
