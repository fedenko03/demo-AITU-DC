from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.hashers import check_password

from api.views import confirmed_order, canceled_order
from keytaker.models import Orders, History, Room
from django.contrib import messages
from django.utils import timezone

from keytaker.views import check_room
from main.models import PIN
from user.models import MainUser


def getOrders():
    last_orders = Orders.objects.filter(
        is_available=True,
        is_confirm=False,
        orders_timestamp__gte=timezone.now() - timezone.timedelta(minutes=5)
    ).order_by('orders_timestamp')

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
            "orders_timestamp": order.orders_timestamp.strftime("%H:%M:%S"),
            "is_confirm": order.is_confirm,
            "is_available": order.is_available
        })
    return orders_list


@login_required(login_url='loginMain')
def homeMain(request):
    orders_list = getOrders()
    return render(request, 'home-main.html', {
        'orders_list': orders_list
    })


@login_required(login_url='loginMain')
def settingsMain(request):
    if request.method == "POST":
        if 'change_password' in request.POST:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            checkPassword = check_password(old_password, request.user.password)
            if checkPassword:
                user_obj = User.objects.get(username=request.user)
                user_obj.set_password(new_password)
                user_obj.save()
                messages.success(request, 'Password changed successfully. Please log in again.')
                return redirect('loginMain')
            else:
                messages.error(request, 'Неверный пароль')
                return redirect('settingsMain')
    orders_list = getOrders()
    return render(request, 'settings.html', {
        'orders_list': orders_list
    })


def loginMain(request):
    if request.user.is_authenticated:
        return redirect('homeMain')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=username).first()

        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('loginMain')
        if not user_obj.is_staff:
            messages.error(request, 'This form for admins only.')
            return redirect('loginMain')

        user = authenticate(username=username, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('loginMain')
        login(request, user)
        return redirect('homeMain')
    return render(request, 'login-main.html')


@login_required(login_url='loginMain')
def logoutMain(request):
    logout(request)
    return redirect('loginMain')


@login_required(login_url='loginMain')
def confirm_takeroom(request, pk):
    order_obj = Orders.objects.filter(id=pk).first()
    if not order_obj:
        messages.error(request, 'Заявка не найдена')
        return redirect('homeMain')
    error = check_room(order_obj.room.name)
    if error:
        order_obj.is_available = False
        order_obj.save()
        messages.error(request, error)
        canceled_order(error)
        return redirect('homeMain')
    if order_obj.is_confirm or not order_obj.is_available or timezone.now() - order_obj.orders_timestamp >= timezone.timedelta(
            minutes=5):
        order_obj.is_available = False
        order_obj.save()
        canceled_order('Данная заявка больше неактуальна')
        messages.error(request, 'Данная заявка больше неактуальна')
        return redirect('homeMain')

    if request.method == 'POST':
        code = request.POST.get('code')
        order_obj = Orders.objects.filter(confirmation_code=code).first()

        if not order_obj:
            messages.error(request, 'Неверный код или заявка')
            return redirect('confirm-takeroom', pk)

        order_obj.is_available = False
        order_obj.is_confirm = True
        history = History.objects.create(
            room=order_obj.room,
            fullname=order_obj.user.full_name,
            is_verified=True,
            role=order_obj.user.role,
            date=timezone.now()
        )
        room_obj = Room.objects.filter(name=order_obj.room.name).first()
        room_obj.is_occupied = True
        room_obj.save()
        history.save()
        order_obj.save()
        confirmed_order('Заявка подтверждена успешно')
        messages.success(request, 'Заявка подтверждена успешно')
        return redirect('homeMain')
    else:
        orders_list = {'id': pk,
                       'room': order_obj.room.name,
                       'note': order_obj.note,
                       'user': {
                           'name': order_obj.user.full_name,
                           'email': order_obj.user.email
                       },
                       "orders_timestamp": order_obj.orders_timestamp,
                       "is_confirm": order_obj.is_confirm
                       }
        print(orders_list)
        orders1_list = getOrders()
        return render(request, 'confirm-takeroom-main.html', {
            'orders_list': orders1_list,
            'order': orders_list
        })


def cancel_takeroomMain(request, pk):
    order_obj = Orders.objects.filter(id=pk).first()
    if order_obj:
        order_obj.is_available = False
        order_obj.save()
        msg = 'Заявка успешно отклонена.'
        canceled_order('Заявка была отклонена. Попробуйте снова')
        messages.error(request, msg)
        return redirect('homeMain')
    return redirect('confirm-takeroom', pk)


@login_required(login_url='loginMain')
def historyMain(request):
    history_obj = History.objects.order_by('-date')[:10]
    orders_list = getOrders()
    print(orders_list)
    return render(request, 'history-main.html', {
        'orders_list': orders_list,
        'history_obj': history_obj
    })


@login_required(login_url='loginMain')
def usersMain(request):
    users_obj = MainUser.objects.order_by('full_name')[:10]
    orders_list = getOrders()
    return render(request, 'users-main.html', {
        'orders_list': orders_list,
        'users_obj': users_obj
    })


@login_required(login_url='loginMain')
def roomsMain(request):
    rooms_obj = Room.objects.order_by('name')[:10]
    orders_list = getOrders()
    return render(request, 'rooms-main.html', {
        'orders_list': orders_list,
        'rooms_obj': rooms_obj
    })


@login_required(login_url='loginMain')
def pinLocked(request):
    if request.method == "POST":
        code = request.POST.get("pincode")
        code_obj = PIN.objects.filter(code=code).first()
        if not code_obj:
            messages.error(request, 'Неверный PIN-код')
            return redirect('pinLocked')
        code_obj.is_locked = False
        code_obj.save()
        return redirect('homeMain')
    return render(request, 'pin.html')


@login_required(login_url='loginMain')
def PinLock(request, code):
    pinLock_obj = PIN.objects.first()
    if pinLock_obj.is_locked:
        messages.error(request, 'Доступ был заблокирован ранее')
        return redirect('homeMain')

    if code.isdigit() and 4 <= len(code) <= 10:
        pinLock_obj.is_locked = True
        pinLock_obj.code = code
        pinLock_obj.save()
        return redirect('pinLocked')
    else:
        messages.error(request, 'PIN-код должен содержать от 4 до 10 цифр.')
        return redirect('homeMain')
