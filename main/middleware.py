from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from main.models import PIN


class NotFoundMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated and request.user.is_staff:
            if response.status_code == 404:
                return redirect('not_foundMain')
        else:
            if response.status_code == 404:
                return redirect('not_foundUser')
        return response


class PinCodeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/main/') or \
                request.path.startswith('/keytaker/') or \
                request.path.startswith('/keyreturner/') or \
                request.path.startswith('/admin/') or \
                request.path.startswith('/media/'):
            pinLock_obj = PIN.objects.first()
            if request.user.is_authenticated and not request.user.is_staff:
                return redirect('home')
            if request.user.is_authenticated and pinLock_obj.is_locked:
                if request.path != reverse('pinLocked'):
                    return redirect(reverse('pinLocked'))
            if not request.user.is_authenticated:
                if request.path != reverse('loginMain'):
                    return redirect('loginMain')
        elif request.path.startswith('/api/'):
            if not request.user.is_authenticated:
                return redirect('homeMain')
            if not request.user.is_staff:
                return redirect('home')
        elif request.path.startswith('/'):
            if not request.user.is_authenticated:
                if request.path != reverse('login_user') and \
                        request.path != reverse('register') and \
                        request.path != reverse('confirm_registration'):
                    return redirect('login_user')
            if request.user.is_authenticated and request.user.is_staff:
                return redirect('homeMain')

        response = self.get_response(request)
        return response
