from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import math

from keytaker.models import History, Room
from keytaker.views import getOrders


def keyreturnerMain(request):
    history_obj = History.objects.filter(
        is_return=False
    )

    history_list = []
    for history in history_obj:
        history_list.append({
            'id': history.id,
            'date': history.date.strftime("%D (%H:%M)"),
            'fullname': history.fullname,
            'room': history.room.name,
            'role': history.role.name,
            'is_return': history.is_return
        })
    orders_list = getOrders()
    return render(request, 'keyreturner-main.html', {
        'orders_list': orders_list,
        'history_obj': history_list[:5],
        'history_count': len(history_obj)
    })


def returnKeyConfirm(request, id):
    history_obj = History.objects.filter(id=id).first()
    if not history_obj:
        messages.error(request, 'Заявка не найдена')
        return redirect('keyreturnerMain')
    history_obj.is_return = True
    room_obj = Room.objects.filter(name=history_obj.room.name).first()
    room_obj.is_occupied = False
    history_obj.save()
    room_obj.save()
    messages.success(request, 'Возвращение ключа подтверждено')
    return redirect('keyreturnerMain')
