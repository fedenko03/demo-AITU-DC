import math
import random
import string
import json
import asyncio

import pytz
from django.http import JsonResponse
from django.utils import timezone

from keytaker.consumers import WSNewOrder, WSCanceledORConfirmedOrder
from keytaker.models import *

local_tz = pytz.timezone('Asia/Almaty')


def generate_code():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))


def check_room(room):
    if not room:
        return "Empty string"
    room_obj = Room.objects.filter(name=room).first()
    if not room_obj:
        return "Not found"
    if not room_obj.is_visible:
        return "The room is unavailable"
    return None


def getHistoryData(request, page, step):
    # step=1 - next
    # step=0 - previous
    history_obj = History.objects.filter(
        is_return=False
    )
    history_list = []
    objectsOnPage = 5
    fromPage = page
    toPage = 1
    fromHstr = fromPage * objectsOnPage
    toHstr = toPage * objectsOnPage

    if step == 1:
        print("step = 1")
        if page + 1 <= math.ceil(len(history_obj) / objectsOnPage):
            fromHstr = page * objectsOnPage  # 5
            toHstr = fromHstr + objectsOnPage  # 10
        else:
            return JsonResponse({'history_obj': history_list})
    elif step == 0:
        print("step = 0")
        if page - 1 >= 1:  # 2 page
            fromHstr = (page-2) * objectsOnPage  # 0
            toHstr = fromHstr + objectsOnPage  # 5
        else:
            return JsonResponse({'history_obj': history_list})

    # convert queryset to list of dictionaries
    for history in history_obj:
        history_list.append({
            'id': history.id,
            'date': history.date.astimezone(local_tz).strftime("%D (%H:%M)"),
            'fullname': history.fullname,
            'room': history.room.name,
            'role': history.role.name,
            'is_return': history.is_return
        })

    history_slice = history_list[fromHstr:toHstr]
    return JsonResponse({'history_obj': history_slice})


def searchRoom(request, room):
    error = check_room(room)
    if error:
        return JsonResponse({'error': error})
    room = Room.objects.filter(name=room).first()
    history_obj = History.objects.filter(
        room=room,
        is_return=False
    )
    history_list = []
    for history in history_obj:
        history_list.append({
            'id': history.id,
            'date': history.date.astimezone(local_tz).strftime("%D (%H:%M)"),
            'fullname': history.fullname,
            'room': history.room.name,
            'role': history.role.name,
            'is_return': history.is_return
        })

    return JsonResponse({'history_obj': history_list})


def new_order_notify(order_obj):
    for consumer in WSNewOrder.consumers:
        asyncio.run(consumer.send(text_data=json.dumps({
            'order_id': order_obj.id,
            'room_name': order_obj.room.name,
            'note': order_obj.note,
            'time': order_obj.orders_timestamp.astimezone(local_tz).strftime("%H:%M:%S"),
            'user_full_name': order_obj.user.full_name,
            'user_email': order_obj.user.email
        })))


def canceled_order(email, msg):
    for consumer in WSCanceledORConfirmedOrder.consumers:
        asyncio.run(consumer.send(text_data=json.dumps({
            'email': email,
            'msg_id': 1,
            'msg': msg
        })))


def confirmed_order(email, msg):
    for consumer in WSCanceledORConfirmedOrder.consumers:
        asyncio.run(consumer.send(text_data=json.dumps({
            'email': email,
            'msg_id': 2,
            'msg': msg
        })))


def get_last5_orders(request):
    current_time = timezone.now()
    time_diff = timezone.timedelta(minutes=5)

    last_5_orders = Orders.objects.filter(
        is_available=True,
        orders_timestamp__gte=current_time-time_diff
    ).order_by('-orders_timestamp')[:5]

    orders_list = []
    for order in last_5_orders:
        orders_list.append({'room': order.room.name,
                            'note': order.note,
                            'user': {
                                'name': order.user.full_name,
                                'email': order.user.email
                            },
                            "orders_timestamp": order.orders_timestamp,
                            "is_confirm": order.is_confirm,
                            })

    new_order_obj = Orders.objects.create(
        room=Room.objects.filter(name='C1.2.239K').first(),
        confirmation_code=generate_code(),
        note="",
        user=MainUser.objects.filter(email='211524@astanait.edu.kz').first(),
        orders_timestamp=timezone.now()
    )
    new_order_obj.save()
    new_order_notify(new_order_obj)

    return JsonResponse(orders_list, safe=False)


def takeroom_isVar_changed(request):
    settings_obj = SettingsKeyTaker.objects.first()
    return JsonResponse({'variable_is_confirm': settings_obj.is_confirm})


def cancel_takeroom(request, pk):
    order_obj = Orders.objects.filter(id=pk).first()
    if order_obj:
        if not order_obj.is_confirm or order_obj.is_available:
            msg = 'Successfully'
            canceled_order(order_obj.user.email, 'Заявка была отклонена. Попробуйте снова')
            order_obj.is_available = False
            order_obj.save()
        else:
            msg = 'Already canceled'
    else:
        msg = 'Not found'
    return JsonResponse({
        'email': order_obj.user.email,
        'msg_id': 1,
        'msg': msg
    })
