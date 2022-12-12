# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm, SignUpForm
from django.core.mail import send_mail
from django.views import View
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth.models import User
from django.contrib import messages


def login_view(request):
    form = LoginForm(request.POST or None)

    msg = None

    if request.method == "POST":

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'

    return render(request, "accounts/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            email = form.cleaned_data.get("email")
            user = authenticate(username=username, password=raw_password)
            user.is_active = False
            user.save()
            uid = urlsafe_base64_encode(force_bytes(user.email))
            domain = get_current_site(request).domain
            link = reverse('activate', kwargs={
                           'uid': uid,
                           #    'token': token_generator.make_token(user)
                           })
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

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()

    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


class VertificationView(View):
    def get(self, request, uid):
        id = force_str(urlsafe_base64_decode(uid))
        user = User.objects.get(email=id)

        # if not token_generator.check_token(user, token):
        #     return redirect('login'+'?message='+'User already activated')

        if user.is_active:
            msg = 'Your emailemail has successfully vertify'
            return render(request, 'accounts/activate.html', {"msg": msg})
        else:
            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
        return redirect('login')
