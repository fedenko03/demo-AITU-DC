from django.shortcuts import render, redirect
from .forms import TakeRoom


def form_page_one(request):
    if request.method == 'POST':
        form = TakeRoom(request.POST)
        if form.is_valid():
            request.session['form_data'] = form.cleaned_data
            return redirect('form_page_two')
    else:
        form = TakeRoom()
    return render(request, 'page1.html', {'form': form})


def form_page_two(request):
    if request.method == 'POST':
        form = TakeRoom(request.POST)
        if form.is_valid():
            request.session['form_data'].update(form.cleaned_data)
            return redirect('form_page_three')
    else:
        form_data = request.session.get('form_data', {})
        form = TakeRoom(initial=form_data)
    return render(request, 'page2.html', {'form': form})


def form_success(request):
    form_data = request.session.get('form_data', {})
    # Обработка данных формы
    return render(request, 'page3.html', {'form_data': form_data})
