# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from curses import window
import webbrowser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import LoginForm, SignUpForm
from django.core.mail import send_mail
from django.views import View
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.cache import cache_control


def login_view(request):
    msg = None
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
               webbrowser.open_new_tab('/admin/')
               webbrowser.open('/')
            elif user.is_staff:
                return redirect("/")
    else:
        form = LoginForm()

    return render(request, "accounts/login.html", {"form": form})


@cache_control(max_age=3600)
def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                msg = "A user with the given email already exists"
                success = False
                return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})
            else:
                username = form.cleaned_data.get("username")
                raw_password = form.cleaned_data.get("password1")
                user = User.objects.create_user(
                    username=username, password=raw_password, email=email)
                user.is_active = False
                user.save()
                uid = urlsafe_base64_encode(force_bytes(user.email))
                domain = get_current_site(request).domain
                link = reverse('activate', kwargs={
                    'uid': uid})
                activate_url = 'http://'+domain+link
                email_subject = 'active your clothes account'
                email_body = 'hi '+user.username + \
                    ' please verify your account by clicking the link below\n' + activate_url
                send_mail(
                    email_subject,
                    email_body,
                    '',
                    [email],
                    fail_silently=False,
                )

                msg = 'User created - please <a href="/login">login</a>.'
                success = True

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


class VertificationView(View):
    def get(self, request, uid):
        id = force_str(urlsafe_base64_decode(uid))
        user = get_object_or_404(User, email=id)

        if user.is_active:
            msg = 'Your emailemail has successfully vertify'
            return render(request, 'accounts/activate.html', {"msg": msg})
        else:
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
        return redirect('login')
