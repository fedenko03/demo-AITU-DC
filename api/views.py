import math
import random
import string
import json
import asyncio
from datetime import timedelta

import pytz
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from AITUDC import settings
from keytaker.consumers import WSNewOrder, WSCanceledORConfirmedOrder, WebSocketQR
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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

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
            fromHstr = (page - 2) * objectsOnPage  # 0
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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

    current_time = timezone.now()
    time_diff = timezone.timedelta(minutes=5)

    last_5_orders = Orders.objects.filter(
        is_available=True,
        orders_timestamp__gte=current_time - time_diff
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
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

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


def get_room_schedule(request, room_number):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'}, status=403)
    try:
        room = Room.objects.filter(map_id=room_number).first()
        # room = get_object_or_404(Room, name=room_number, is_study_room=True)
        if not room:
            return JsonResponse({'error': 'Room not found'})

        role_names = []
        for role in room.role.all():
            role_names.append(role.name)

        user_fullname = ''
        if room.is_occupied:
            history_obj = History.objects.filter(
                room=room,
                is_return=False
            ).first()
            if history_obj:
                user_fullname = history_obj.fullname
        else:
            user_fullname = None

        room_info = {
            'name': room.name,
            'description': room.description,
            'is_occupied': room.is_occupied,
            'user_fullname': user_fullname,
            'is_study_room': room.is_study_room,
            'is_visible': room.is_visible,
            'role': role_names
        }

        schedule_list = []
        if room.is_study_room:
            schedule = StudyRoomSchedule.objects.filter(room=room).order_by('start_time')

            for cell in schedule:
                if cell.professor:
                    schedule_list.append({
                        'start_time': cell.start_time.strftime('%H:%M'),
                        'end_time': cell.end_time.strftime('%H:%M'),
                        'professor': {
                            'name': cell.professor.full_name,
                            'email': cell.professor.email
                        },
                        'status': cell.status
                    })
                else:
                    schedule_list.append({
                        'start_time': cell.start_time.strftime('%H:%M'),
                        'end_time': cell.end_time.strftime('%H:%M'),
                        'professor': None,
                        'status': cell.status
                    })
        return JsonResponse({
            'room': room_info,
            'schedule': schedule_list
        })
    except StudyRoomSchedule.DoesNotExist:
        return JsonResponse({'error': 'Error'})


def create_reservation(request, room_name, start_time_input, is_take):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

    try:
        room = Room.objects.get(name=room_name, is_study_room=True)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'})

    schedule = StudyRoomSchedule.objects.filter(room=room)
    if not schedule.exists():
        return JsonResponse({'error': 'The room does not have a schedule'})

    try:
        start_time = datetime.datetime.strptime(start_time_input, '%H:%M').time()
    except ValueError:
        return JsonResponse({'error': 'Invalid start time value'})

    time_slot = schedule.filter(start_time=start_time).first()
    if not time_slot:
        return JsonResponse({'error': 'The room does not have a schedule at this time'})

    if time_slot.status != 'free':
        return JsonResponse({'error': 'The selected time slot is not available'})

    start_time = datetime.datetime.strptime(start_time_input, '%H:%M').time()
    schedule_start_time = datetime.datetime.combine(datetime.date.today(), time_slot.start_time)
    schedule_start_time = timezone.make_aware(schedule_start_time, timezone.get_current_timezone())
    time_to_reservation = schedule_start_time - timezone.now()

    # print(abs(time_to_reservation))
    # print(time_to_reservation)

    if time_to_reservation < -timezone.timedelta(minutes=60):
        return JsonResponse({'error': 'It is too late to take the key.'})

    if is_take:
        if time_to_reservation < timezone.timedelta(minutes=30):
            if room.is_occupied:
                return JsonResponse({'error': 'The key is not available.'})
        else:
            return JsonResponse({'error': 'The key is not available.'})

    key = generate_code()
    reservation = Reservation.objects.create(
        room=room,
        start_time=start_time,
        key=key,
        created_at=timezone.now(),
        is_take=is_take
    )
    reservation.save()

    return JsonResponse({'reservation': reservation.key})


def booking_change_is_take(request, key, is_take):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

    try:
        reservation_obj = Reservation.objects.get(key=key)
    except Reservation.DoesNotExist:
        return JsonResponse({'error': 'Reservation not found.'})

    try:
        room = Room.objects.get(name=reservation_obj.room, is_study_room=True)
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'})

    schedule_start_time = datetime.datetime.combine(datetime.date.today(), reservation_obj.start_time)
    schedule_start_time = timezone.make_aware(schedule_start_time, timezone.get_current_timezone())
    time_to_reservation = schedule_start_time - timezone.now()

    if room.is_occupied:
        return JsonResponse({'error': 'Ключа нет у охраны.'})

    if time_to_reservation > timezone.timedelta(minutes=30):
        return JsonResponse({'error': 'Взять ключ можно только если осталось менее 30 минут до начала занятия.'})

    # Check if the reservation is still valid (created less than 5 minutes ago)
    time_diff = timezone.now() - reservation_obj.created_at
    if time_diff > timezone.timedelta(minutes=5):
        return JsonResponse({'error': 'The reservation has expired.'})

    # Check if the reservation is not yet activated
    if reservation_obj.is_active:
        return JsonResponse({'error': 'The reservation has already been confirmed.'})

    reservation_obj.is_take = is_take
    reservation_obj.save()

    status_list = []
    status_list.append({'notification_type': 'key_booking',
                        'data': {
                            'link_confirm': 'link',
                            'qr_url': settings.MEDIA_URL + 'bookingQR.png',
                            'timestamp': (reservation_obj.created_at + timedelta(minutes=5)).astimezone(
                                local_tz).strftime("%H:%M:%S %d.%m.%Y"),
                            'room': reservation_obj.room.name,
                            'time': reservation_obj.start_time.strftime("%H"),
                            'is_take': reservation_obj.is_take
                        }})
    for consumer in WebSocketQR.consumers:
        asyncio.run(consumer.send(text_data=json.dumps(status_list)))
    return JsonResponse({'success': is_take})


def get_rooms_status(request, floor):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'})
    if not request.user.is_staff:
        return JsonResponse({'error': 'Access denied'})

    rooms_list = Room.objects.filter(floor=floor).all().order_by('name')
    rooms_status_list = []
    for room in rooms_list:
        status = ''

        if not room.is_visible:
            status = 'not_visible'
        # elif room.is_study_room:
        #     status = 'study_room'
        elif room.is_occupied:
            status = 'occupied'
        else:
            status = 'free'

        rooms_status_list.append({
            'room': room.name,
            'map_id': room.map_id,
            'status': status
        })
    return JsonResponse({'rooms_status_list': rooms_status_list})
