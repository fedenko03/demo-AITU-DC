from django.shortcuts import render, redirect
from django.utils import timezone

from .models import *
from .forms import ChooseRoom, ChooserData
import qrcode
import random
import string


def generate_code():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))


def step2(request):
    if request.method == 'POST':
        form = ChooseRoom(request.POST)
        if form.is_valid():
            # save form data to session
            request.session['room'] = form.cleaned_data['room']
            # redirect to the next page
            return redirect('step3')
    else:
        form = ChooseRoom()
    return render(request, 'step2.html', {'form': form})


def step3(request):
    if request.method == 'POST':
        return redirect('step4')
    else:
        room = request.session.get('room')
        settings_obj = SettingsKeyTaking.objects.first()
        settings_obj.confirmation_code = generate_code()
        settings_obj.code_timestamp = timezone.now()
        settings_obj.is_confirm = False

        # settings_obj = SettingsKeyTaking.objects.create(
        #     confirmation_code=generate_code(),
        #     code_timestamp=timezone.now(),

        settings_obj.save()
        link_confirm = "http://127.0.0.1:8000/user/confirm_keytaking/token="+settings_obj.confirmation_code
        img = qrcode.make(link_confirm)
        img.save("media/qr.png")
        qr_image = True
    return render(request, 'step3.html', {
        'qr_image': qr_image,
        'room': room,
        'link': link_confirm
    })


def step4(request):
    if request.method == 'POST':
        form = ChooserData(request.POST)
        if form.is_valid():
            request.session['fullname'] = form.cleaned_data['fullname']
            request.session['status'] = form.cleaned_data['status']
            request.session['date'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            history = History(
                room=request.session.get('room'),
                fullname=request.session.get('fullname'),
                status=request.session.get('status'),
                date=request.session.get('date')
            )
            history.save()
            return redirect('success')
    else:
        form = ChooserData()
    room = request.session.get('room')
    return render(request, 'step4.html', {
        'form': form,
        'room': room
    })


def success(request):
    room = request.session.get('room')
    fullname = request.session.get('fullname')
    status = request.session.get('status')
    date = request.session.get('date')
    request.session.flush()
    return render(request, 'success.html', {
        'room': room,
        'fullname': fullname,
        'status': status,
        'date': date
    })
