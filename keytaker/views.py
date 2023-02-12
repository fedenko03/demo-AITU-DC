import json

from django.contrib.auth.decorators import *
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from .consumers import WSNewOrder
from .models import *
from .forms import ChooseRoom, ChooserData
import qrcode
import random
import string
from django.http import JsonResponse
import asyncio

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import Orders


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
@user_passes_test(is_staff, login_url='login_user')
def takeroom2(request):
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
    return render(request, 'takeroom2.html', {'form': form})


@login_required(login_url='loginMain')
@user_passes_test(is_staff, login_url='login_user')
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

        link_confirm = "http://" + request.get_host() + "/confirm_keytaking/token=" + settings_obj.confirmation_code
        img = qrcode.make(link_confirm)
        img.save("media/qr.png")
        qr_image = True

        return render(request, 'takeroom3.html', {
            'qr_image': qr_image,
            'room': room,
            'link': link_confirm,
            'is_confirm': 'false'
        })


@login_required(login_url='loginMain')
@user_passes_test(is_staff, login_url='login_user')
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
        return render(request, 'takeroom4.html', {
            'form': form,
            'room': room
        })


@login_required(login_url='loginMain')
@user_passes_test(is_staff, login_url='login_user')
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
        return render(request, 'takeroomFinal.html', {
            'history': last_history_obj,
            'error': None
        })


@login_required(login_url='loginMain')
@user_passes_test(is_staff, login_url='login_user')
def takeroom_isVar_changed(request):
    settings_obj = SettingsKeyTaker.objects.first()
    return JsonResponse({'variable_is_confirm': settings_obj.is_confirm})


@login_required(login_url='loginMain')
def new_order_notify(order_obj):
    for consumer in WSNewOrder.consumers:
        asyncio.run(consumer.send(text_data=json.dumps({
            'order_id': order_obj.id,
            'room_name': order_obj.room.name,
            'note': order_obj.note,
            'time': order_obj.orders_timestamp.strftime("%H:%M:%S"),
            'user_full_name': order_obj.user.full_name
        })))


@login_required(login_url='loginMain')
@user_passes_test(is_staff, login_url='login_user')
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
                            "is_confirm": order.is_confirm
                            })

    # new_order_obj = Orders.objects.create(
    #     room=Room.objects.first(),
    #     confirmation_code=generate_code(),
    #     note=generate_code(),
    #     user=MainUser.objects.first(),
    #     orders_timestamp=timezone.now()
    # )
    # new_order_obj.save()
    #
    # new_order_notify(new_order_obj)
    return JsonResponse(orders_list, safe=False)

