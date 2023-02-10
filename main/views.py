from django.shortcuts import render


def homeMain(request):
    return render(request, 'home-main.html')
