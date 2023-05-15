import json
import random
import string
import uuid
from datetime import timedelta

import pytz
from django.contrib.auth import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail

from AITUDC import settings
from api.views import new_order_notify
from keyreturner.models import SettingsKeyReturner
from keytaker.consumers import WSCanceledORConfirmedOrder, WSGetUser, WSUpdateBookingStatus, WebSocketQR
from keytaker.views import check_room
from keytaker.forms import ChooserData
from .models import *
from keytaker.models import *
import asyncio

local_tz = pytz.timezone('Asia/Almaty')


def generate_code():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def generate_TakeRoomcode():
    # Generate a random confirmation code
    return ''.join(random.choices(string.digits, k=6))


def is_available_to_takeroom():
    last_orders = Orders.objects.filter(
        is_available=True,
        is_confirm=False,
        orders_timestamp__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).order_by('-orders_timestamp')
    if len(last_orders) < 2:
        return True
    else:
        return False


def is_not_staff(user):
    return not user.is_staff


def role_checker(room, role):
    print(room)
    print(role)
    has_role = False
    room_obj = Room.objects.filter(name=room).first()
    for rol1 in room_obj.role.all():
        print(rol1)
        if rol1.name == role or rol1.name == 'All':
            has_role = True
            break
    if not has_role:
        return "Ваш статус не позволяет взять ключ от этого кабинета"
    return None


def not_foundUser(request):
    return render(request, 'notfound404User.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        try:
            if fullname == '':
                messages.error(request, 'Incorrect fullname.')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.error(request, 'This email is already in use.')
                return redirect('register')

            if not email.endswith('@astanait.edu.kz'):
                messages.error(request, 'Email must be from @astanait.edu.kz domain.')
                return redirect('register')

            user_obj = User(username=email, email=email, first_name=fullname)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = MainUser.objects.create(
                user=user_obj,
                full_name=fullname,
                email=email,
                auth_token=auth_token,
                confirmation_code=generate_code(),
                code_timestamp=timezone.now(),
                role=Role.objects.filter(name=role).first()
            )
            profile_obj.save()

            # Email confirmation
            subject = 'Confirm your email address'
            message = f'Enter this code to confirm your account: {profile_obj.confirmation_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [profile_obj.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('confirm_registration')

        except Exception as e:
            print(e)
            messages.error(request, 'Произошла неизвестная ошибка')
            return redirect('confirm_registration')

    return render(request, 'register.html', {
        'form': ChooserData()
    })


def confirm_registration(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user = MainUser.objects.get(confirmation_code=code)
            if timezone.now() - user.code_timestamp <= timezone.timedelta(minutes=5):
                user.is_active = True
                user.save()
                login(request, user.user)
                return redirect('home')
            else:
                return render(request, 'confirm_registration.html', {'error': 'Code expired'})
        except MainUser.DoesNotExist:
            return render(request, 'confirm_registration.html', {'error': 'Invalid code'})
    return render(request, 'confirm_registration.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()

        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login_user')
        if user_obj.is_staff:
            messages.error(request, 'This form not for admin.')
            return redirect('login_user')

        profile_obj = MainUser.objects.filter(user=user_obj).first()

        if not profile_obj.is_active:
            messages.success(request, 'Profile is not verified. Please, enter the code from email or register again.')
            return redirect('login_user')

        user = authenticate(username=email, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login_user')

        login(request, user)
        return redirect('home')

    return render(request, 'login_user.html')


@login_required(login_url='login_user')
def logout_user(request, ):
    logout(request)
    return redirect('login_user')


def qr_checker(request, settings_obj):
    if settings_obj.is_confirm:
        error = 'Сканированный QR код уже был подтверждён. Вернитесь к 1 шагу.'
        return error
    if timezone.now() - settings_obj.code_timestamp >= timezone.timedelta(minutes=5):
        error = 'Срок действия QR кода истёк.'
        return error
    if not settings_obj.type == 'QR':
        error = 'Невозможно активировать используя QR-код, попробуйте сначала.'
        settings_obj.error = error
        settings_obj.is_confirm = True
        settings_obj.save()
        return error
    if check_room(settings_obj.room.name):
        error = 'Комната выбрана неверно или уже занята'
        settings_obj.error = error
        settings_obj.is_confirm = True
        settings_obj.save()
        return error
    user_obj = MainUser.objects.filter(email=request.user.username).first()
    error = role_checker(settings_obj.room.name, user_obj.role.name)
    return error


@login_required(login_url='login_user')
def confirm_keytaking(request, confirmation_code):  # step 4
    try:
        settings_obj = SettingsKeyTaker.objects.filter(confirmation_code=confirmation_code).first()

        if settings_obj:
            error = qr_checker(request, settings_obj)
            if error:
                messages.error(request, error)
                return redirect('home')
            settings_obj.is_confirm = True
            profile_obj = MainUser.objects.filter(email=request.user.username).first()
            if not profile_obj:
                messages.error(request, 'Пользователь не найден или не авторизован')
                return redirect('home')

            if settings_obj.room.is_study_room:
                current_datetime = timezone.now().astimezone(local_tz)

                # Определяем начало текущего интервала времени.
                # Фильтруем ячейки по указанному интервалу времени
                print(current_datetime.minute)
                if (current_datetime.minute >= 0) and (current_datetime.minute < 30):
                    interval_start_time = str(current_datetime.hour) + ':00'
                    cells = StudyRoomSchedule.objects.get(room=settings_obj.room, start_time=interval_start_time)

                    print('1 ' + interval_start_time)
                    if cells.status == 'free':
                        cells.status = 'reserved'
                        cells.professor = profile_obj
                        cells.save()
                    else:
                        if not cells.professor.email == profile_obj.email:
                            messages.error(request,
                                           'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                               current_datetime.hour) + ':00 до ' + str(current_datetime.hour) + ':50')
                            return redirect('home')
                elif (current_datetime.minute >= 30) and (current_datetime.minute < 50):
                    interval_start_time1 = str(current_datetime.hour) + ':00'
                    interval_start_time2 = str(current_datetime.hour + 1) + ':00'
                    cells1 = StudyRoomSchedule.objects.get(room=settings_obj.room, start_time=interval_start_time1)
                    cells2 = StudyRoomSchedule.objects.get(room=settings_obj.room, start_time=interval_start_time2)
                    print('2 ' + interval_start_time1 + ' + ' + interval_start_time2)
                    if cells2.status == 'free':
                        cells2.status = 'reserved'
                        cells2.professor = profile_obj
                        cells2.save()

                    if not cells1.professor and not cells2.professor:
                        messages.error(request,
                                       'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                           current_datetime.hour) + ' до ' + str(current_datetime.hour + 1) + ':50')
                        return redirect('home')

                    error_flag = False
                    if not cells1.professor and cells2.professor:
                        if not cells2.professor.email == profile_obj.email:
                            error_flag = True
                        else:
                            error_flag = False
                    elif cells1.professor and not cells2.professor:
                        if not cells1.professor.email == profile_obj.email:
                            error_flag = True
                        else:
                            error_flag = False

                    if error_flag:
                        messages.error(request,
                                       'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета.')
                        return redirect('home')
                else:
                    interval_start_time = str(current_datetime.hour + 1) + ':00'
                    cells = StudyRoomSchedule.objects.get(room=settings_obj.room, start_time=interval_start_time)
                    print('3 ' + interval_start_time)
                    if cells.status == 'free':
                        cells.status = 'reserved'
                        cells.professor = profile_obj
                        cells.save()
                    else:
                        if not cells.professor.email == profile_obj.email:
                            messages.error(request,
                                           'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                               current_datetime.hour + 1) + ':00 до ' + str(
                                               current_datetime.hour + 1) + ':50')
                            return redirect('home')

            history = History.objects.create(
                room=settings_obj.room,
                fullname=profile_obj.full_name,
                is_verified=True,
                role=Role.objects.filter(name=profile_obj.role.name).first(),
                user=profile_obj,
                date=timezone.now()
            )
            room_obj = Room.objects.filter(name=settings_obj.room.name).first()
            room_obj.is_occupied = True
            room_obj.save()
            settings_obj.save()
            history.save()
            messages.success(request, 'Заявка на взятие ключа подтверждена успешно.')
            return redirect('home')
        else:
            messages.error(request, 'Заявки не существует, возможно её уже активировали ')
            return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')


@login_required(login_url='login_user')
def settings_user(request):
    if request.method == "POST":
        if 'change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            confirm_new_password = request.POST.get('confirm_new_password')
            if not new_password == confirm_new_password:
                messages.error(request, 'Новый пароль не совпадает')
                return redirect('settings_user')
            if len(new_password) < 6:
                messages.error(request, 'Пароль должен содержать не менее 6 символов.')
                return redirect('settings_user')
            if len(new_password) > 20:
                messages.error(request, 'Пароль должен содержать не более 20 символов.')
                return redirect('settings_user')
            checkPassword = check_password(old_password, request.user.password)
            if checkPassword:
                user_obj = User.objects.get(username=request.user)
                user_obj.set_password(new_password)
                user_obj.save()
                messages.success(request, 'Password changed successfully. Please log in again.')
                return redirect('login_user')
            else:
                messages.error(request, 'Неверный пароль')
                return redirect('settings_user')

        if 'change_fullname' in request.POST:
            fullname = request.POST.get('fullname')
            password = request.POST.get('password')

            name_without_spaces = fullname.replace(" ", "")
            if len(name_without_spaces) < 5:
                messages.error(request, 'ФИО должно содержать не менее 5 символов.')
                return redirect('settings_user')

            if len(name_without_spaces) > 35:
                messages.error(request, 'ФИО должно содержать не более 35 символов.')
                return redirect('settings_user')

            if not fullname.replace(" ", "").isalpha():
                messages.error(request, 'Имя может содержать только буквы и пробелы.')
                return redirect('settings_user')

            checkPassword = check_password(password, request.user.password)
            if checkPassword:
                user_obj = User.objects.get(username=request.user)
                user_obj.first_name = fullname
                user_obj.save()
                profile_obj = MainUser.objects.filter(email=request.user.username).first()
                profile_obj.full_name = fullname
                profile_obj.save()
                messages.success(request, 'Fullname changed successfully.')
                return redirect('settings_user')
            else:
                messages.error(request, 'Неверный пароль')
                return redirect('settings_user')
    return render(request, 'settings_user.html')


@login_required(login_url='login_user')
def home(request):
    step = request.session.get('step')
    code = request.session.get('code')
    room = request.session.get('room')
    timestamp_code = request.session.get('timestamp_code')
    order_obj = Orders.objects.filter(confirmation_code=code).first()

    if not step:
        request.session['step'] = 1
    if not code:
        request.session['code'] = ''
    if not timestamp_code:
        request.session['timestamp_code'] = ''
    if not room:
        request.session['room'] = ''
    if order_obj:
        if order_obj.is_confirm or not order_obj.is_available:
            request.session['step'] = 1
            request.session['code'] = ''
            request.session['timestamp_code'] = ''
            request.session['room'] = ''
        if timezone.now() - order_obj.orders_timestamp >= timezone.timedelta(minutes=5):
            request.session['step'] = 1
            request.session['code'] = ''
            request.session['timestamp_code'] = ''
            request.session['room'] = ''
            messages.error(request, "Время ожидания истекло. Попробуйте сначала.")
    else:
        request.session['step'] = 1
        request.session['code'] = ''
        request.session['timestamp_code'] = ''
        request.session['room'] = ''

    if request.method == 'POST':
        if step == 1:
            room = request.POST.get('room')
            note = request.POST.get('note')

            if not is_available_to_takeroom():
                messages.error(request, 'На данный момент все места для заявок заняты. Попробуйте через 5 минут.')
                return redirect('home')

            error = check_room(room)
            if error:
                messages.error(request, error)
                return redirect('home')

            user_obj = MainUser.objects.filter(email=request.user.username).first()
            error = role_checker(room, user_obj.role.name)
            if error:
                messages.error(request, error)
                return redirect('home')

            room_obj = Room.objects.filter(name=room).first()
            if room_obj.is_study_room:
                current_datetime = timezone.now().astimezone(local_tz)

                # Определяем начало текущего интервала времени.
                # Фильтруем ячейки по указанному интервалу времени
                print(current_datetime.minute)
                if (current_datetime.minute >= 0) and (current_datetime.minute < 30):
                    interval_start_time = str(current_datetime.hour) + ':00'
                    try:
                        cells = StudyRoomSchedule.objects.get(room=room_obj, start_time=interval_start_time)
                    except StudyRoomSchedule.DoesNotExist:
                        messages.error(request, 'Сейчас взять ключ от кабинета не получится. Попробуйте позже')
                        return redirect('home')

                    if not cells:
                        messages.error(request, 'Сейчас взять ключ от кабинета не получится. Попробуйте позже')
                        return redirect('home')

                    print('1 ' + interval_start_time)
                    if not cells.professor:
                        messages.error(request,
                                       'Кабинет не забронирован на ' + str(current_datetime.hour) + ':00. Для брони подойдите к охране.')
                        return redirect('home')
                    if not cells.professor.email == user_obj.email:
                        messages.error(request,
                                       'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                           current_datetime.hour) + ':00 до ' + str(current_datetime.hour) + ':50')
                        return redirect('home')
                elif (current_datetime.minute >= 30) and (current_datetime.minute < 50):
                    interval_start_time1 = str(current_datetime.hour) + ':00'
                    interval_start_time2 = str(current_datetime.hour + 1) + ':00'
                    try:
                        cells1 = StudyRoomSchedule.objects.get(room=room_obj, start_time=interval_start_time1)
                        cells2 = StudyRoomSchedule.objects.get(room=room_obj, start_time=interval_start_time2)
                    except StudyRoomSchedule.DoesNotExist:
                        messages.error(request, 'Сейчас взять ключ от кабинета не получится. Попробуйте позже')
                        return redirect('home')

                    print('2 ' + interval_start_time1 + ' + ' + interval_start_time2)

                    if not cells1.professor and not cells2.professor:
                        messages.error(request,
                                       'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                           current_datetime.hour) + ':00 до ' + str(current_datetime.hour + 1) + ':50')
                        return redirect('home')

                    error_flag = False
                    if not cells1.professor and cells2.professor:
                        if not cells2.professor.email == user_obj.email:
                            error_flag = True
                        else:
                            error_flag = False
                    elif cells1.professor and not cells2.professor:
                        if not cells1.professor.email == user_obj.email:
                            error_flag = True
                        else:
                            error_flag = False

                    if error_flag:
                        messages.error(request,
                                       'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                           current_datetime.hour) + ':00 до ' + str(current_datetime.hour + 1) + ':50')
                        return redirect('home')
                else:
                    interval_start_time = str(current_datetime.hour + 1) + ':00'
                    try:
                        cells = StudyRoomSchedule.objects.get(room=room_obj, start_time=interval_start_time)
                    except StudyRoomSchedule.DoesNotExist:
                        messages.error(request, 'Сейчас взять ключ от кабинета не получится. Попробуйте позже')
                        return redirect('home')

                    if not cells:
                        messages.error(request, 'Сейчас взять ключ от кабинета не получится. Попробуйте позже')
                        return redirect('home')

                    print('3 ' + interval_start_time)
                    if not cells.professor:
                        messages.error(request,
                                       'Кабинет не забронирован на ' + str(current_datetime.hour+1) + ':00. Для брони подойдите к охране.')
                        return redirect('home')
                    if not cells.professor.email == user_obj.email:
                        messages.error(request,
                                       'Вы не можете сейчас взять ключ от кабинета, так как Вас нет в расписании кабинета с ' + str(
                                           current_datetime.hour + 1) + ':00 до ' + str(
                                           current_datetime.hour + 1) + ':50')
                        return redirect('home')

            if len(note) > 50:
                messages.error(request, 'Ваш комментарий слишком длинный')
                return redirect('home')

            code_generated = generate_TakeRoomcode()
            request.session['code'] = code_generated

            request.session['room'] = room

            later = timezone.now() + timedelta(minutes=5)  # Add 5 minutes to the current time
            later_formatted = later.astimezone(local_tz).strftime('%H:%M:%S')
            request.session['timestamp_code'] = later_formatted
            print(later_formatted)

            new_order_obj = Orders.objects.create(
                room=Room.objects.filter(name=room).first(),
                confirmation_code=code_generated,
                note=note,
                user=MainUser.objects.filter(email=request.user.username).first(),
                orders_timestamp=timezone.now()
            )
            new_order_obj.save()
            new_order_notify(new_order_obj)
            request.session['step'] = 2

            return redirect('home')

    profile_obj = MainUser.objects.filter(email=request.user.username).first()
    role = profile_obj.role if profile_obj else None
    print(role)
    room_list = Room.objects.filter(
        is_visible=True,
        is_occupied=False,
        role__in=[profile_obj.role]
    ).all().order_by('name')
    return render(request, 'home-user.html', {
        'room_list': room_list,
        'profile': profile_obj,
        'step': request.session.get('step'),
        'code': request.session.get('code'),
        'room': request.session.get('room'),
        'timestamp_code': request.session.get('timestamp_code')
    })


@login_required(login_url='login_user')
def history_user(request):
    user_obj = MainUser.objects.filter(email=request.user.username).first()
    history_obj = History.objects.filter(user=user_obj).order_by('-date')[:15]
    return render(request, 'history_user.html', {
        'history_obj': history_obj
    })


@login_required(login_url='login_user')
def key_return_get_user(request, token):
    settings_obj = SettingsKeyReturner.objects.filter(token=token).first()
    if not settings_obj:
        messages.error(request, 'Заявка не найдена')
        return redirect('home')
    user_obj = MainUser.objects.filter(email=request.user.username).first()
    if not user_obj:
        messages.error(request, 'Пользователь не найден')
        return redirect('home')
    if timezone.now() - settings_obj.token_timestamp >= timezone.timedelta(minutes=5):
        messages.error(request, 'Срок действия QR кода истёк.')
        return redirect('home')
    settings_obj.user = user_obj
    settings_obj.step = 2
    settings_obj.in_process = True
    settings_obj.save()
    ws_get_user(request, user_obj)
    messages.success(request, 'Успешно! Выберите нужную заявку на экране администратора')
    return redirect('home')


def ws_get_user(request, user_obj):
    settings_obj = SettingsKeyReturner.objects.filter(user=user_obj).first()
    if not settings_obj:
        messages.error(request, 'Заявка недействительна. Попробуйте сначала')
    history_obj = History.objects.filter(
        is_return=False,
        user=user_obj
    ).all()

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
    for consumer in WSGetUser.consumers:
        asyncio.run(consumer.send(text_data=json.dumps(history_list)))

    status_list = []
    status_list.append({'notification_type': 'mobile',
                        'data': 'none'})
    for consumer in WebSocketQR.consumers:
        asyncio.run(consumer.send(text_data=json.dumps(status_list)))


@login_required(login_url='login_user')
def reserve_studyroom(request, key):
    status_list = []
    try:
        reservation = Reservation.objects.get(key=key)
    except Reservation.DoesNotExist:
        messages.error(request, "Reservation not found")
        return redirect('home')

    # Check if the user has sufficient permissions to make a reservation in the room
    user_obj = MainUser.objects.filter(email=request.user.username).first()

    room = reservation.room

    if role_checker(room, user_obj.role.name):
        messages.error(request, "You don't have sufficient permissions to make a reservation in this room")
        return redirect('home')

    # Check if the room has a schedule and the time slot is free
    studyroom_schedule = StudyRoomSchedule.objects.filter(
        room=room,
        start_time=reservation.start_time
    ).first()
    if not studyroom_schedule:
        status_list.append({'status': 'error',
                            'key': reservation.key})
        for consumer in WSUpdateBookingStatus.consumers:
            asyncio.run(consumer.send(text_data=json.dumps(status_list)))
        messages.error(request, 'The room ' + room.name + ' does not have a schedule or this time slot.')
        return redirect('home')
    if studyroom_schedule.status != 'free':
        status_list.append({'status': 'error',
                            'key': reservation.key})
        for consumer in WSUpdateBookingStatus.consumers:
            asyncio.run(consumer.send(text_data=json.dumps(status_list)))
        messages.error(request, "The selected time slot is not available.")
        return redirect('home')

    # Check if the reservation is still valid (created less than 5 minutes ago)
    time_diff = timezone.now() - reservation.created_at
    if time_diff > timezone.timedelta(minutes=5):
        status_list.append({'status': 'error',
                            'key': reservation.key})
        for consumer in WSUpdateBookingStatus.consumers:
            asyncio.run(consumer.send(text_data=json.dumps(status_list)))
        messages.error(request, "The reservation has expired.")
        return redirect('home')

    # Check if the reservation is not yet activated
    if reservation.is_active:
        messages.error(request, "The reservation has already been confirmed.")
        return redirect('home')

    # Check if the user wants to take the key and if the time to the reservation is less than 30 minutes
    # and if there is a key in the history

    schedule_start_time = datetime.datetime.combine(datetime.date.today(), reservation.start_time)
    schedule_start_time = timezone.make_aware(schedule_start_time, timezone.get_current_timezone())
    time_to_reservation = schedule_start_time - timezone.now()

    # print(abs(time_to_reservation))
    # print(time_to_reservation)

    if time_to_reservation < -timezone.timedelta(minutes=60):
        status_list.append({'status': 'error',
                            'key': reservation.key})
        for consumer in WSUpdateBookingStatus.consumers:
            asyncio.run(consumer.send(text_data=json.dumps(status_list)))
        messages.error(request, "It's too late to make a reservation.")
        return redirect('home')

    if reservation.is_take:
        # print(time_to_reservation)
        # print(timezone.timedelta(minutes=30))
        if time_to_reservation < timezone.timedelta(minutes=30):
            if room.is_occupied:
                messages.error(request, "The key is not available.")
                return redirect('home')
            else:
                new_history = History.objects.create(
                    room=room,
                    fullname=user_obj.full_name,
                    is_verified=True,
                    role=Role.objects.filter(name=user_obj.role.name).first(),
                    user=user_obj,
                    date=timezone.now()
                )
                room.is_occupied = True
                room.save()
                new_history.save()
                messages.success(request, "You have taken the key for the room.")

    # Create the reservation in the schedule
    studyroom_schedule.status = 'reserved'
    studyroom_schedule.professor = user_obj
    studyroom_schedule.save()

    # Activate the reservation
    reservation.is_active = True
    reservation.save()

    messages.success(request, "The reservation has been successfully activated.")
    status_list.append({'status': 'success',
                        'key': reservation.key})
    for consumer in WSUpdateBookingStatus.consumers:
        asyncio.run(consumer.send(text_data=json.dumps(status_list)))
    return redirect('home')
