from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
# Create your views here.


from .forms import CreateUserForm, UserForm, ProfileForm, RateForm
from .models import *
from random import choice

from django.db.models import Avg


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
                user = form.save()
                username = form.cleaned_data.get('username')
                UserProfile.objects.create(
                    user=user,
                    )
                messages.success(request, 'Account was created for ' + user.username)
                return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('homepage')


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
            [EMAIL_HOST_USER],  # To Email
        )
        context = {'message_name': message_name}
        return render(request, 'accounts/homepage-contact.html', context)
    else:
        return render(request, 'accounts/homepage-contact.html', {})


def home(request):
    context = {}
    return render(request, 'accounts/home.html', context)


def profile(request):
    
    skills = request.user.userprofile.skill.all()
    reviews = Review.objects.filter(user_reviewed=request.user.userprofile)
    reviews_avg = reviews.aggregate(Avg('rate'))['rate__avg']
    reviews_count = reviews.count()
    context = {'reviews_avg':reviews_avg, 'reviews_count':reviews_count, 'skills':skills}

    return render(request, 'accounts/profile.html', context)


def userrandom(request):
    randomly = choice([i for i in range(1, 5) if i not in [request.user.id, 1]])
    name = User.objects.get(id=randomly).username
    context = {'name': name}
    return render(request, 'accounts/random.html', context)




def edit_profile(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.userprofile) 
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,('Your profile was successfully updated!'))
        else:
            messages.error(request,('Unable to complete request'))
        return redirect ('profile')
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.userprofile)        
    context = {'user_form':user_form, 'profile_form': profile_form}
    return render(request, 'accounts/edit-profile.html', context)


def users_profile(request):
    user_p = get_user_model()
    users = user_p.objects.all()
    all_users = users.exclude(username=request.user)
    



    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user_l = UserProfile.objects.get(id = user_id)
        request.user.userprofile.desired_user.add(user_l.id)
        messages.success(request,(f'{user_l} added to Starred Users.'))
        return redirect ('users_profile')
    context = {'all_users': all_users}
    return render(request, 'accounts/users.html', context)






def starred_users(request):
    user_list = request.user.userprofile.desired_user.all()
    context = {'user_list': user_list}
    return render(request, 'accounts/starred_users.html', context)



def remove_desireuser(request):  
    context = {}
    return render(request, 'accounts/starred_users.html', context)



def user_profile(request, pk):
    user = UserProfile.objects.get(id=pk)
    reviews = Review.objects.filter(user_reviewed=user)
    reviews_avg = reviews.aggregate(Avg('rate'))['rate__avg']
    reviews_count = reviews.count()
    skills = user.skill.all()
    context = {'user': user, 'reviews_avg':reviews_avg, 'reviews_count':reviews_count, 'skills':skills}
    return render(request, 'accounts/user_profile.html', context)



def Rate(request, pk):
    user_reviewd = UserProfile.objects.get(id = pk)
    user = request.user.userprofile
    form = RateForm()

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rate = form.save(commit=False)
            rate.user_reviewed = user_reviewd
            rate.user_reviewing = user
            rate.save()
            return redirect('users_profile')
        

    context = {'form':form, 'user_reviewd':user_reviewd}
    return render(request, 'accounts/rate_user.html', context)




def RemoveStaredUser(request, pk):
    desired_user = UserProfile.objects.get(id=pk)
    user = request.user.userprofile
    if request.method == 'POST':
        user.desired_user.remove(desired_user)
        return redirect('starred_users')
   
    context = {'desired_user': desired_user}
    return render(request, 'accounts/RemoveDesiredUser.html', context)




def admin_users(request):
    user_p = get_user_model()
    users = user_p.objects.all()
    all_users = users.exclude(username=request.user)

    context = {'all_users': all_users}
    return render(request, 'accounts/admin-users.html', context)



def delete_user(request, pk):
    user = User.objects.get(id=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_users')

    context = {'user': user}
    return render(request, 'accounts/delete_user.html', context)


def about(request):
    context = {}
    return render(request, 'accounts/about.html', context )
