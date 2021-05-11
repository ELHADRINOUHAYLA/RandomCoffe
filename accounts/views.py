from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
# Create your views here.
from .forms import CreateUserForm

from random import choice


def homepage(request):
    context = {}
    return render(request, 'accounts/homepage.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is Incorrect')
    context = {}
    return render(request, 'accounts/login.html', context)


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == "POST":
        message_name = request.POST['name']
        message_email = request.POST['email']
        message = request.POST['message']
        # send an email
        send_mail(
            message_name,  # subject
            message,  # message
            message_email,  # from email
            ['nohaila1999elhadri@gmail.com'],  # To Email
        )
        context = {'message_name': message_name}
        return render(request, 'accounts/homepage-contact.html', context)
    else:
        return render(request, 'accounts/homepage-contact.html', {})


def home(request):
    context = {}
    return render(request, 'accounts/home.html', context)


def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)


def userrandom(request):
    randomly = choice([i for i in range(1, 5) if i not in [request.user.id, 1]])
    name = User.objects.get(id=randomly).username
    context = {'name': name}
    return render(request, 'accounts/random.html', context)
