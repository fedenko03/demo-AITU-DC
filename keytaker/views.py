import asyncio
import json
from datetime import timedelta

import pytz
from django.contrib.auth.decorators import *
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from .consumers import WSNewOrder, WebSocketQR
from .models import *
from .forms import ChooseRoom, ChooserData
import qrcode
import random
import string
from .models import Orders

from django.conf import settings
import io
# from azure.storage.blob import BlockBlobService

local_tz = pytz.timezone('Asia/Almaty')


def getOrders():
    last_orders = Orders.objects.filter(
        is_available=True,
        is_confirm=False,
        orders_timestamp__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).order_by('-orders_timestamp')

    orders_list = []
    for order in last_orders:
        orders_list.append({
            'id': order.id,
            'room': order.room.name,
            'note': order.note,
            'user': {
                'name': order.user.full_name,
                'email': order.user.email
            },
            "orders_timestamp": order.orders_timestamp.astimezone(local_tz).strftime("%H:%M:%S"),
            "is_confirm": order.is_confirm,
            "is_available": order.is_available
        })
    return orders_list


def generate_code():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))


def check_fullnameAndRole(fullname, role, room):
    # Check if the variable contains only latinic, kazakh or russian letters and spaces
    if not all(map(lambda char: char.isalpha() or char.isspace(), fullname)):
        return "The variable can only contain latinic, kazakh or russian letters and spaces."
    # Check if the length of the variable is within the range [4, 50]
    if not 4 <= len(fullname) <= 50:
        return "The length of the variable must be between 4 and 50 characters."
    # Check role
    if not Role.objects.filter(name=role).first():
        return "Your role does not exist"

    has_role = False
    room_obj = Room.objects.filter(name=room).first()
    for rol1 in room_obj.role.all():
        if rol1.name == role or rol1.name == 'All':
            has_role = True
            break
    if not has_role:
        return "Ваш статус не позволяет взять ключ от этого кабинета"

    # If both conditions are satisfied, return None
    return None


def check_room(room):
    if not room:
        return "Вы не выбрали комнату"
    room_obj = Room.objects.filter(name=room).first()
    if not room_obj:
        return "Комната " + room + " не найдена"
    if room_obj.is_occupied:
        return "Комната " + room + " уже занята"
    if not room_obj.is_visible:
        return "Комната " + room + " недоступна для выбора"
    return None


def check_time_out(request, code_timestamp):
    if timezone.now() - code_timestamp >= timezone.timedelta(minutes=5):
        return "Время ожидания истекло. Попробуйте сначала."
    return None


def clear_session(request):
    del request.session['room']


def is_staff(user):
    return user.is_staff


@login_required(login_url='loginMain')
def takeroom2(request):
    # create_empty_cells()
    # clear_room_schedule()
    # fill_room_schedule()

    settings_obj = SettingsKeyTaker.objects.first()
    settings_obj.confirmation_code = generate_code()
    settings_obj.in_process = True
    settings_obj.is_confirm = False
    if request.method == 'POST':
        form = ChooseRoom(request.POST)

        if form.is_valid():
            room = form.cleaned_data['room']

            error = check_room(room)
            if error:
                messages.error(request, error)
                return redirect('takeroom2')

            settings_obj.step = 3
            settings_obj.save()
            request.session['room'] = room
            return redirect('takeroom3')
    else:
        settings_obj.step = 2
        settings_obj.save()
        form = ChooseRoom()
    orders_list = getOrders()

    rooms_list = Room.objects.order_by('name', 'floor')
    return render(request, 'takeroom2.html', {
        'orders_list': orders_list,
        'form': form,
        'rooms_obj': rooms_list
    })


@login_required(login_url='loginMain')
def takeroom3(request):
    settings_obj = SettingsKeyTaker.objects.first()

    if not settings_obj.in_process:
        return redirect('takeroom2')

    room = request.session.get('room')

    if settings_obj.step != 3:
        settings_obj.step = 2
        settings_obj.is_confirm = False
        settings_obj.in_process = False
        settings_obj.confirmation_code = generate_code()
        settings_obj.save()
        messages.error(request, 'Соблюдайте очередность шагов.')
        return redirect('takeroom2')

    error = check_room(room)
    if error:
        messages.error(request, error)
        return redirect('takeroomFinal')

    if request.method == 'POST':
        error = check_time_out(request, settings_obj.code_timestamp)
        if error:
            messages.error(request, error)
            return redirect('takeroomFinal')

        settings_obj.step = 4
        settings_obj.type = 'Manually'
        settings_obj.save()
        return redirect('takeroom4')
    else:

        settings_obj.confirmation_code = generate_code()
        settings_obj.code_timestamp = timezone.now()
        settings_obj.room = Room.objects.filter(name=room).first()
        settings_obj.is_confirm = False
        settings_obj.type = 'QR'
        settings_obj.step = 3
        settings_obj.error = ''
        settings_obj.save()

        protocol = 'https' if request.is_secure() else 'http'
        link_confirm = f'{protocol}://{request.get_host()}/confirm_keytaking/token={settings_obj.confirmation_code}'
        print(link_confirm)
        img = qrcode.make(link_confirm)
        img.save("media/qr.png")

        status_list = []
        status_list.append({'notification_type': 'key_taker',
                            'data': {
                                'link_confirm': link_confirm,
                                'qr_url': settings.MEDIA_URL + 'qr.png',
                                'timestamp': (settings_obj.code_timestamp + timedelta(minutes=5)).astimezone(
                                    local_tz).strftime("%H:%M:%S %d.%m.%Y"),
                                'room': settings_obj.room.name
                            }})
        for consumer in WebSocketQR.consumers:
            asyncio.run(consumer.send(text_data=json.dumps(status_list)))

        # blob_bytes = io.BytesIO()
        # img.save(blob_bytes, format='PNG')
        # blob_bytes.seek(0)
        # blob_service_client = BlockBlobService(account_name='demoaitustorage',
        #                                        account_key='8VleNnuJtHCquOzk8yMbYk3KKu8SbpInPhXiCcFGzKzZ53TMjUVoMtaSjfySdAwFaftp4vvM9ENZ+AStR+RpHw==')
        # blob_service_client.create_blob_from_bytes(container_name='media', blob_name='qr.png', blob=blob_bytes.read())

        qr_image = True

        orders_list = getOrders()
        return render(request, 'takeroom3.html', {
            'orders_list': orders_list,
            'qr_image': qr_image,
            'room': room,
            'link': link_confirm,
            'is_confirm': 'false',
            'media_url': settings.MEDIA_URL
        })


@login_required(login_url='loginMain')
def takeroom4(request):
    settings_obj = SettingsKeyTaker.objects.first()
    if not settings_obj.in_process:
        return redirect('takeroom2')

    if request.method == 'POST':
        form = ChooserData(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            role = form.cleaned_data['role']
            room = request.session.get('room')

            error = check_room(room)
            if error:
                messages.error(request, error)
                return redirect('takeroomFinal')

            error = check_time_out(request, settings_obj.code_timestamp)
            if error:
                messages.error(request, error)
                return redirect('takeroomFinal')

            error = check_fullnameAndRole(fullname, role, room)
            if error:
                messages.error(request, error)
                return redirect('takeroom4')

            settings_obj = SettingsKeyTaker.objects.first()
            settings_obj.type = 'Manually'
            settings_obj.step = 5
            settings_obj.is_confirm = True
            settings_obj.save()

            history = History.objects.create(
                room=Room.objects.filter(name=room).first(),
                fullname=fullname,
                is_verified=False,
                role=Role.objects.filter(name=role).first(),
                date=timezone.now()
            )
            room_obj = Room.objects.filter(name=room).first()
            room_obj.is_occupied = True
            room_obj.save()
            history.save()
            clear_session(request)
            return redirect('takeroomFinal')
    else:
        if settings_obj.step != 4:
            settings_obj.step = 2
            settings_obj.is_confirm = False
            settings_obj.in_process = False
            settings_obj.confirmation_code = generate_code()
            settings_obj.save()
            messages.error(request, 'Соблюдайте очередность шагов.')
            return redirect('takeroom2')

        form = ChooserData()
        room = request.session.get('room')

        orders_list = getOrders()
        return render(request, 'takeroom4.html', {
            'orders_list': orders_list,
            'form': form,
            'room': room
        })


@login_required(login_url='loginMain')
def takeroomFinal(request):
    settings_obj = SettingsKeyTaker.objects.first()

    if not settings_obj.in_process:
        return redirect('takeroom2')

    if not settings_obj.is_confirm:
        settings_obj.confirmation_code = generate_code()
        settings_obj.save()
        return redirect('takeroom2')

    if settings_obj.step != 5 and settings_obj.type == 'Manually':
        settings_obj.step = 2
        settings_obj.in_process = False
        settings_obj.confirmation_code = generate_code()
        settings_obj.save()
        messages.error(request, 'Соблюдайте очередность шагов.')
        return redirect('takeroom2')
    last_history_obj = History.objects.last()
    settings_obj.in_process = False
    if settings_obj.type == 'QR':
        settings_obj.step = 2
        settings_obj.save()
        return render(request, 'takeroomFinal.html', {
            'history': last_history_obj,
            'error': settings_obj.error
        })
    else:
        settings_obj.step = 2
        settings_obj.save()

        orders_list = getOrders()
        return render(request, 'takeroomFinal.html', {
            'orders_list': orders_list,
            'history': last_history_obj,
            'error': None
        })


def create_empty_cells():
    rooms = Room.objects.filter(is_study_room=True)
    for room in rooms:
        start_time = datetime.time(8, 0)
        end_time = datetime.time(22, 0)
        while start_time < end_time:
            cell = StudyRoomSchedule.objects.create(
                room=room,
                start_time=start_time,
                end_time=(datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=50)).time(),
                status='free'
            )
            cell.save()
            start_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=60)).time()


def fill_room_schedule():
    rooms = Room.objects.filter(is_study_room=True)
    for room in rooms:
        start_time = datetime.time(8, 0)
        end_time = datetime.time(22, 0)
        while start_time < end_time:
            try:
                # Trying to get schedule for this room and time
                schedule = Schedule.objects.get(day=datetime.date.today().weekday()+1, room=room, start_time=start_time)
                status = 'lesson'
                professor = schedule.professor
            except Schedule.DoesNotExist:
                # If schedule not exists then create empty cell
                status = 'free'
                professor = None
            cell = StudyRoomSchedule.objects.create(
                room=room,
                start_time=start_time,
                end_time=(datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=50)).time(),
                status=status,
                professor=professor
            )
            cell.save()
            start_time = (datetime.datetime.combine(datetime.date.today(), start_time) + datetime.timedelta(minutes=60)).time()


def clear_room_schedule():
    StudyRoomSchedule.objects.all().delete()


# source venv/Scripts/activate
# daphne -b 0.0.0.0 -p 8020 AITUDC.asgi:application
