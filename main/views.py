from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render, get_object_or_404

from keytaker.models import Orders, History, Room
from django.contrib import messages
from django.utils import timezone

from keytaker.views import check_room
from user.models import MainUser
from user.views import canceled_order


def is_staff(user):
    return user.is_staff


@login_required(login_url='loginMain')
def homeMain(request):
    return render(request, 'home-main.html')


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
    order_obj = get_object_or_404(Orders, id=pk)
    if order_obj.is_confirm or not order_obj.is_available or \
            timezone.now() - order_obj.orders_timestamp >= timezone.timedelta(minutes=5):
        order_obj.is_available = False
        order_obj.save()
        messages.error(request, 'Данная заявка больше неактуальна')
        return redirect('homeMain')

    if request.method == 'POST':
        code = request.POST.get('code')
        order_obj = Orders.objects.filter(confirmation_code=code).first()

        if not order_obj:
            messages.error(request, 'Неверный код или заявка')
            return redirect('confirm-takeroom', pk)

        error = check_room(order_obj.room.name)
        if error:
            order_obj.is_available = False
            order_obj.save()
            messages.error(request, error)
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
        return render(request, 'confirm-takeroom-main.html', {
            'order': orders_list
        })


def cancel_takeroom(request, pk):
    order_obj = Orders.objects.filter(id=pk).first()
    if order_obj:
        if not order_obj.is_confirm or order_obj.is_available:
            msg = 'Successfully'
            canceled_order('Заявка была отклонена. Попробуйте снова')
            order_obj.is_available = False
            order_obj.save()
        else:
            msg = 'Already canceled'
    else:
        msg = 'Not found'
    return JsonResponse({
        'msg_id': 1,
        'msg': msg
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
    return render(request, 'history-main.html', {
        'history_obj': history_obj
    })


@login_required(login_url='loginMain')
def usersMain(request):
    users_obj = MainUser.objects.order_by('full_name')[:10]
    return render(request, 'users-main.html', {
        'users_obj': users_obj
    })


@login_required(login_url='loginMain')
def roomsMain(request):
    rooms_obj = Room.objects.order_by('name')[:10]
    return render(request, 'rooms-main.html', {
        'rooms_obj': rooms_obj
    })


@login_required(login_url='loginMain')
def pinLocked(request):
    return render(request, 'pin.html')
