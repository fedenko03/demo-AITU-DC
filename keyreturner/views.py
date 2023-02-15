from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
import math

from keytaker.models import History, Room


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
            'email': history.user.email,
            'room': history.room.name,
            'role': history.role.name,
            'is_return': history.is_return
        })
    return render(request, 'keyreturner-step1.html', {
        'history_obj': history_list[:5],
        'history_count': len(history_obj)
    })


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
            'date': history.date.strftime("%D (%H:%M)"),
            'fullname': history.fullname,
            'email': history.user.email,
            'room': history.room.name,
            'role': history.role.name,
            'is_return': history.is_return
        })

    history_slice = history_list[fromHstr:toHstr]
    return JsonResponse({'history_obj': history_slice})


def check_room(room):
    if not room:
        return "Empty string"
    room_obj = Room.objects.filter(name=room).first()
    if not room_obj:
        return "Not found"
    if not room_obj.is_occupied:
        return "The room is free"
    if not room_obj.is_visible:
        return "The room is unavailable"
    return None


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
            'date': history.date.strftime("%D (%H:%M)"),
            'fullname': history.fullname,
            'email': history.user.email,
            'room': history.room.name,
            'role': history.role.name,
            'is_return': history.is_return
        })

    return JsonResponse({'history_obj': history_list})


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
