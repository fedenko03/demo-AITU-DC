import json
import random
import string
import uuid

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail

from AITUDC import settings
from keytaker.consumers import WSCanceledORConfirmedOrder
from keytaker.views import check_room, new_order_notify
from keytaker.forms import ChooserData
from .models import *
from keytaker.models import *
import asyncio


def generate_code():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def is_available_to_takeroom():
    last_orders = Orders.objects.filter(
        is_available=True,
        is_confirm=False,
        orders_timestamp__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).order_by('-orders_timestamp')
    if len(last_orders) < 5:
        return True
    else:
        return False


def is_not_staff(user):
    return not user.is_staff


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
            messages.error(request, e)
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


def role_checker(room, role):
    has_role = False
    room_obj = Room.objects.filter(name=room).first()
    for role1 in room_obj.role.all():
        if role1.name == role or role1.name == 'All':
            has_role = True
            break
    if not has_role:
        return "Ваш статус не позволяет взять ключ от этого кабинета"


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
        error = 'Выбранная комната выбрана неверно или уже занята'
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
            messages.error(request, 'Заявки не существует, возможно её уже активировали '+confirmation_code)
            return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')


@login_required(login_url='login_user')
def home(request):
    step = request.session.get('step')
    code = request.session.get('code')
    order_obj = Orders.objects.filter(confirmation_code=code).first()

    if not step:
        request.session['step'] = 1
    if not code:
        request.session['code'] = ''
    if order_obj:
        if order_obj.is_confirm or not order_obj.is_available:
            request.session['step'] = 1
            request.session['code'] = ''
        if timezone.now() - order_obj.orders_timestamp >= timezone.timedelta(minutes=5):
            request.session['step'] = 1
            request.session['code'] = ''
            messages.error(request, "Время ожидания истекло. Попробуйте сначала.")
    else:
        request.session['step'] = 1
        request.session['code'] = ''

    if request.method == 'POST':
        if step == 1:
            room = request.POST.get('room')
            note = request.POST.get('note')

            if not is_available_to_takeroom():
                messages.error((request, 'На данный момент все места для заявок заняты. Попробуйте через 5 минут.'))

            error = check_room(room)
            if error:
                messages.error(request, error)
                return redirect('home')

            code_generated = generate_code()
            request.session['code'] = code_generated

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
    return render(request, 'home-user.html', {
        'profile': profile_obj,
        'step': request.session.get('step'),
        'code': request.session.get('code')
    })


def canceled_order(msg):
    for consumer in WSCanceledORConfirmedOrder.consumers:
        asyncio.run(consumer.send(text_data=json.dumps({
            'msg_id': 1,
            'msg': msg
        })))


def confirmed_order(msg):
    for consumer in WSCanceledORConfirmedOrder.consumers:
        asyncio.run(consumer.send(text_data=json.dumps({
            'msg_id': 2,
            'msg': msg
        })))
