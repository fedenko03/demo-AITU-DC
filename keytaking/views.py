from django.shortcuts import render, redirect
from .forms import ChooseRoom


def step2(request):
    if request.method == 'POST':
        form = ChooseRoom(request.POST)
        if form.is_valid():
            # save form data to session
            request.session['room'] = form.cleaned_data['room']
            # redirect to the next page
            return redirect('success')
    else:
        form = ChooseRoom()
    return render(request, 'step2.html', {'form': form})


def success(request):
    # retrieve form data from session
    room = request.session.get('room')
    # process the form data
    # ...
    # clear the session data
    request.session.flush()
    return render(request, 'success.html', {
        'room': room
    })
