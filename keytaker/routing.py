from django.urls import path

from .consumers import WSConsumer, WSNewOrder, WSCanceledORConfirmedOrder, WSGetUser, WSUpdateBookingStatus, WebSocketQR

ws_urlpatterns = [
    path('ws/some_url/', WSConsumer.as_asgi()),
    path('ws/get_user_keyreturner/', WSGetUser.as_asgi()),
    path('ws/new_order/', WSNewOrder.as_asgi()),
    path('ws/canceledOrConfirmed_order/', WSCanceledORConfirmedOrder.as_asgi()),
    path('ws/update_booking_status/', WSUpdateBookingStatus.as_asgi()),
    path('ws/notification_type/', WebSocketQR.as_asgi())
]
