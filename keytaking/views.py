from django.shortcuts import render, redirect
from django.utils import timezone

from .models import History
from .forms import ChooseRoom, ChooserData
import qrcode


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
        img = qrcode.make("https://vk.com")  # qrcode.make(data)
        img.save("media/qr.png")
        qr_image = True
    return render(request, 'step3.html', {
        'qr_image': qr_image,
        'room': room
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
