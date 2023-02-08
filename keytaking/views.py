from django.contrib.auth.decorators import *
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages

from .models import *
from .forms import ChooseRoom, ChooserData
import qrcode
import random
import string
from django.http import JsonResponse


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
    if not Category.objects.filter(name=role).first():
        return "Your role does not exist"

    has_category = False
    room_obj = Room.objects.filter(name=room).first()
    for category in room_obj.category.all():
        if category.name == role or category.name == 'All':
            has_category = True
            break
    if not has_category:
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


def step_checker(request):
    settings_obj = SettingsKeyTaking.objects.first()


def clear_session(request):
    del request.session['room']


def is_staff(user):
    return user.is_staff


@login_required(login_url='login_user')
@user_passes_test(is_staff)
def takeroom2(request):
    if request.method == 'POST':
        form = ChooseRoom(request.POST)

        if form.is_valid():
            room = form.cleaned_data['room']

            error = check_room(room)
            if error:
                messages.error(request, error)
                return redirect('takeroom2')

            request.session['room'] = room
            return redirect('takeroom3')
    else:
        form = ChooseRoom()
    return render(request, 'takeroom2.html', {'form': form})


@login_required(login_url='login_user')
@user_passes_test(is_staff)
def takeroom3(request):
    settings_obj = SettingsKeyTaking.objects.first()
    room = request.session.get('room')

    error = check_room(room)
    if error:
        messages.error(request, error)
        return redirect('takeroomFinal')

    if request.method == 'POST':
        error = check_time_out(request, settings_obj.code_timestamp)
        if error:
            messages.error(request, error)
            return redirect('takeroomFinal')

        settings_obj.type = 'Manually'
        settings_obj.save()
        return redirect('takeroom4')
    else:

        settings_obj.confirmation_code = generate_code()
        settings_obj.code_timestamp = timezone.now()
        settings_obj.room = Room.objects.filter(name=room).first()
        settings_obj.is_confirm = False
        settings_obj.type = 'QR'
        settings_obj.error = ''
        settings_obj.save()

        link_confirm = "http://" + request.get_host() + "/user/confirm_keytaking/token=" + settings_obj.confirmation_code
        img = qrcode.make(link_confirm)
        img.save("media/qr.png")
        qr_image = True

        return render(request, 'takeroom3.html', {
            'qr_image': qr_image,
            'room': room,
            'link': link_confirm,
            'is_confirm': 'false'  # add checker
        })


@login_required(login_url='login_user')
@user_passes_test(is_staff)
def takeroom4(request):
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

            settings_obj = SettingsKeyTaking.objects.first()
            error = check_time_out(request, settings_obj.code_timestamp)
            if error:
                messages.error(request, error)
                return redirect('takeroomFinal')

            error = check_fullnameAndRole(fullname, role, room)
            if error:
                messages.error(request, error)
                return redirect('takeroom4')

            settings_obj = SettingsKeyTaking.objects.first()
            settings_obj.type = 'Manually'
            settings_obj.save()

            history = History.objects.create(
                room=Room.objects.filter(name=room).first(),
                fullname=fullname,
                is_verified=False,
                role=Category.objects.filter(name=role).first(),
                date=timezone.now()
            )
            room_obj = Room.objects.filter(name=room).first()
            room_obj.is_occupied = True
            room_obj.save()
            history.save()
            clear_session(request)
            return redirect('takeroomFinal')
    else:
        form = ChooserData()
        room = request.session.get('room')
        return render(request, 'takeroom4.html', {
            'form': form,
            'room': room
        })


@login_required(login_url='login_user')
@user_passes_test(is_staff)
def takeroomFinal(request):
    settings_obj = SettingsKeyTaking.objects.first()
    last_history_obj = History.objects.last()
    if settings_obj.type == 'QR':
        return render(request, 'takeroomFinal.html', {
            'history': last_history_obj,
            'error': settings_obj.error
        })
    else:
        return render(request, 'takeroomFinal.html', {
            'history': last_history_obj,
            'error': None
        })


def takeroom_isVar_changed(request):
    settings_obj = SettingsKeyTaking.objects.first()
    return JsonResponse({'variable_is_confirm': settings_obj.is_confirm})


# http://172.20.10.2:8020/keytaking/st3/
