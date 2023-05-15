import json
import token
from datetime import timedelta

import pytz
import qrcode
import random
import string

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
import asyncio
import math
from django.conf import settings
import io
from azure.storage.blob import BlockBlobService

from keyreturner.models import SettingsKeyReturner
from keytaker.consumers import WebSocketQR
from keytaker.models import History, Room
from keytaker.views import getOrders

local_tz = pytz.timezone('Asia/Almaty')

def generate_token():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))


# def post(self, request):
#     file = request.FILES['file']
#     filename = file.name
#     file_upload_name = str(uuid.uuid4()) + file.name
#     blob_service_client = BlockBlobService(account_name = 'accountname', account_key='accountkey')
#     blob_service_client.create_blob_from_bytes( container_name = 'container-name', blob_name = file_upload_name, blob = file.read())
#     return JsonResponse( { "status": "success", "uploaded_file_name": file_upload_name}, status=201)


def keyreturnerMain(request):
    history_obj = History.objects.filter(
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
    orders_list = getOrders()

    settings_obj = SettingsKeyReturner.objects.first()
    settings_obj.token = generate_token()
    settings_obj.in_process = False
    settings_obj.error = ''
    settings_obj.step = 1
    settings_obj.user = None
    settings_obj.token_timestamp = timezone.now()
    settings_obj.save()
    print(settings_obj.token)
    link_confirm = "http://" + request.get_host() + "/key_return_get_user/token=" + settings_obj.token
    img = qrcode.make(link_confirm)

    img.save("media/returnerQR.png")

    status_list = []
    status_list.append({'notification_type': 'key_returner',
                        'data': {
                            'link_confirm': link_confirm,
                            'qr_url': settings.MEDIA_URL + 'returnerQR.png',
                            'timestamp': (settings_obj.token_timestamp + timedelta(minutes=5)).astimezone(local_tz).strftime("%H:%M:%S %d.%m.%Y")
                        }})
    for consumer in WebSocketQR.consumers:
        asyncio.run(consumer.send(text_data=json.dumps(status_list)))

    # blob_bytes = io.BytesIO()
    # img.save(blob_bytes, format='PNG')
    # blob_bytes.seek(0)
    # blob_service_client = BlockBlobService(account_name='demoaitustorage', account_key='8VleNnuJtHCquOzk8yMbYk3KKu8SbpInPhXiCcFGzKzZ53TMjUVoMtaSjfySdAwFaftp4vvM9ENZ+AStR+RpHw==')
    # blob_service_client.create_blob_from_bytes(container_name='media', blob_name='returnerQR.png', blob=blob_bytes.read())

    qr_image = True

    return render(request, 'keyreturner-main.html', {
        'orders_list': orders_list,
        'history_obj': history_list[:5],
        'history_count': len(history_obj),
        'qr_image': qr_image,
        'media_url': settings.MEDIA_URL
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



