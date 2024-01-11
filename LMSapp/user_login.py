from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .EmailBackEnd import EmailBackEnd
from .models import *


def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        # check email
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email are Already Exists !')
            return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username are Already exists !')
            return redirect('register')

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')
        user = User(
            username=username,
            email=email,
            first_name=firstname,
            last_name=lastname,

        )

        selected_value = request.POST.get('btnradio')

        if selected_value == 'student':
            user.set_password(password)
            user.save()
            group = Group.objects.get(name="free members")
            user.groups.add(group)
            user.save()

        elif selected_value == 'auther':

            auther = Author(
                name=firstname + " " + lastname,
                user_name=username)
            auther.save()
            user.is_staff = True
            user.save()
            group = Group.objects.get(name="Course Author Group")
            user.groups.add(group)
            user.set_password(password)
            user.save()


        # user.set_password(password)
        # user.save()
        # group = Group.objects.get(name="gold members")
        # user.groups.add(group)
        # user.save()
        else:
            pass
        return redirect('login')

    return render(request, 'registration/register.html')


def DO_LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,
                                         username=email,
                                         password=password)
        if user != None:
            login(request, user)
            if user.groups.filter(name="Course Author Group").exists():
                admin_url = reverse('admin:index')
                return redirect(admin_url)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Email and Password Are Invalid !')
            return redirect('login')


def Profile_Update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Successfully Updated. ')
        return redirect('profile')


def PROFILE(request):
    return render(request, "registration/profile.html")

