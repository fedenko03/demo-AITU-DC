from django.urls import path

from .consumers import WSConsumer, WSNewOrder

ws_urlpatterns = [
    path('ws/some_url/', WSConsumer.as_asgi()),
    path('ws/new_order/', WSNewOrder.as_asgi())
]
