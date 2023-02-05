import random
import string
import uuid

from django.contrib.auth import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail

from AITUDC import settings
from .models import *


def generate_code():
    # Generate a random confirmation code
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))


def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(password)

        try:
            if fullname == '':
                messages.error(request, 'Incorrect fullname.')
                return redirect('register')

            if User.objects.filter(email=email).first():
                messages.error(request, 'This email is already in use.')
                return redirect('register')

            user_obj = User(username=email, email=email, first_name=fullname)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = CustomUser.objects.create(
                user=user_obj,
                full_name=fullname,
                email=email,
                auth_token=auth_token,
                confirmation_code=generate_code(),
                code_timestamp=timezone.now(),
            )
            profile_obj.save()

            # Email confirmation
            subject = 'Confirm your email address'
            message = f'Enter this code to confirm your account: {profile_obj.confirmation_code}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [profile_obj.email]
            send_mail(subject, message, from_email, recipient_list)

            return redirect('confirm')

        except Exception as e:
            print(e)
            messages.error(request, e)
            return redirect('confirm')

    return render(request, 'register.html')


def confirm(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            user = CustomUser.objects.get(confirmation_code=code)
            if timezone.now() - user.code_timestamp <= timezone.timedelta(minutes=20):
                user.is_active = True
                user.save()
                login(request, user.user)
                return redirect('home')
            else:
                return render(request, 'confirm.html', {'error': 'Code expired'})
        except CustomUser.DoesNotExist:
            return render(request, 'confirm.html', {'error': 'Invalid code'})
    return render(request, 'confirm.html')


def login_user(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(email=email).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('login_user')

        profile_obj = CustomUser.objects.filter(user=user_obj).first()

        if not profile_obj.is_active:
            messages.success(request, 'Profile is not verified. Please, enter the code from email or register again.')
            return redirect('login_user')

        user = authenticate(username=email, password=password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('login_user')

        login(request, user)
        return redirect('home')

    return render(request, 'login_user.html')


def logout_user(request):
    logout(request)
    return redirect('login_user')


@login_required(login_url='login_user')
def home(request):
    return render(request, 'home.html')
