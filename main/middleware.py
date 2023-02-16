from django.shortcuts import redirect
from django.urls import reverse

from main.models import PIN


class PinCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/main/') or \
                request.path.startswith('/keytaker/') or\
                request.path.startswith('/keyreturner/') or \
                request.path.startswith('/admin/'):
            pinLock_obj = PIN.objects.first()
            if request.user.is_authenticated and pinLock_obj.is_locked:
                if request.path != reverse('pinLocked'):
                    return redirect(reverse('pinLocked'))

        response = self.get_response(request)
        return response
