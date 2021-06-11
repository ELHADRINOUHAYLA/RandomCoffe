from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from project.settings import EMAIL_HOST_USER
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.

# resset password 

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.http import JsonResponse

from .forms import CreateUserForm, UserForm, ProfileForm, RateForm, PersonalSkillForm, FreeDateForm
from .models import *
from random import choice

from django.db.models import Avg
import json
from django.http import JsonResponse
# -----------------------------------------------------------------

def search_users(request):
    if request.method == 'POST':
        user_p = get_user_model()
        users = user_p.objects.all()
        search_str = json.loads(request.body).get('searchText')
        usersList = users.filter(
            first_name__istartswith=search_str) | users.filter(
            last_name__istartswith=search_str) | users.filter(
            username__istartswith=search_str) 
        data = usersList.values()
        return JsonResponse(list(data), safe=False)


# -----------------------------------------------------------------
def homepage(request):
    context = {}
    return render(request, 'accounts/homepage.html', context)
# -----------------------------------------------------------------

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
# -----------------------------------------------------------------

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('login')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():

                user = form.save(commit=False)
                if Employe.objects.filter(Ref=user.username):
                    user.save()
                    username = form.cleaned_data.get('username')
                    UserProfile.objects.create(
                    user=user,
                     )
                    messages.success(request, 'Account was created for ' + user.username)
                    return redirect('login')
                else:
                    messages.error(request, 'Please make sure your ID is correct')
                    return redirect('register')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)



def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

# -----------------------------------------------------------------
def logoutUser(request):
    logout(request)
    return redirect('login')

# -----------------------------------------------------------------
def contact(request):
    if request.method == "POST":
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        message = request.POST.get('message')


        message_email = 'Email from :' + email + '  Full name:  '  + firstname +'  '+ lastname + '   Phone: '+ phone + ' message:  ' + message

        subject = firstname + lastname
        # send an email
        send_mail(
            subject,  # subject
            message_email,  # message
            email,  # from email
            ['nohaila1999elhadri@gmail.com'],  # To Email
        )
        context = {'firstname': firstname, 'lastname':lastname}
        return render(request, 'accounts/homepage-contact.html', context)
    else:
        return render(request, 'accounts/homepage-contact.html', {})
# -----------------------------------------------------------------
@login_required(login_url='login')
def home(request):
    user_p = get_user_model()
    users = user_p.objects.all()
    freedate = FreeDate.objects.filter(user = request.user)
    starreds = request.user.userprofile.desired_user.all()
    message =" No much Found! Good Luck next Week"
    matched_user = User

    if starreds:
        for u in starreds:
            u_freedate = FreeDate.objects.filter(user=u.user)
            for dates in freedate:
                for matchdates in u_freedate:
                    if dates.FreeTime == matchdates.FreeTime and dates.FreeDay == matchdates.FreeDay:
                        matched_user = u

    else:
        for u in users:
            u_freedate = FreeDate.objects.filter(user = u)
            for dates in freedate:
                for matchdates in u_freedate:
                    if dates.FreeTime == matchdates.FreeTime and dates.FreeDay == matchdates.FreeDay:
                        matched_user = u.userprofile


    context = {'freedate': freedate, 'matched_user': matched_user, 'message':message}
    return render(request, 'accounts/home.html', context)
# -----------------------------------------------------------------
@login_required(login_url='login')
def Freedate(request):
    form = FreeDateForm()
    if request.method == 'POST':
        form = FreeDateForm(request.POST)
        if form.is_valid():
            form2 = form.save(commit=False)
            form2.user = request.user 
            form2.save()
            return redirect('home')
    context = {'form':form}
    return render(request, 'accounts/FreeDate.html', context)


# -----------------------------------------------------------------
@login_required(login_url='login')
def profile(request):
    
    skills = request.user.userprofile.skill.all()
    personalskills = request.user.userprofile.personalskill.all()
    reviews = Review.objects.filter(user_reviewed=request.user.userprofile)
    reviews_avg = reviews.aggregate(Avg('rate'))['rate__avg']
    reviews_count = reviews.count()
    context = {'reviews_avg':reviews_avg, 'reviews_count':reviews_count, 'skills':skills, 'personalskills': personalskills}

    return render(request, 'accounts/profile.html', context)
# -----------------------------------------------------------------
@login_required(login_url='login')
def userrandom(request):
    randomly = choice([i for i in range(1, 5) if i not in [request.user.id, 1]])
    name = User.objects.get(id=randomly).username
    context = {'name': name}
    return render(request, 'accounts/random.html', context)


# -----------------------------------------------------------------
@login_required(login_url='login')
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
# -----------------------------------------------------------------
@login_required(login_url='login')
def admin_edit_profile(request, pk):
    user_p = get_user_model()
    profile = user_p.objects.get(id=pk)
    user_form = UserForm(instance=profile)
    profile_form = ProfileForm(instance=profile.userprofile) 
    if request.method == 'POST':
        user_form = UserForm(request.POST,instance=profile)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,('User profile was successfully updated!'))
        else:
            messages.error(request,('Unable to complete request'))
        return redirect ('admin_users')
    user_form = UserForm(instance=profile)
    profile_form = ProfileForm(instance=profile.userprofile)        
    context = {'user_form':user_form, 'profile_form': profile_form}
    return render(request, 'accounts/admin-edit-profile.html', context)

    

# -----------------------------------------------------------------  

@login_required(login_url='login')
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



# -----------------------------------------------------------------

@login_required(login_url='login')
def starred_users(request):
    user_list = request.user.userprofile.desired_user.all()
    context = {'user_list': user_list}
    return render(request, 'accounts/starred_users.html', context)
# -----------------------------------------------------------------

@login_required(login_url='login')
def remove_desireuser(request):  
    context = {}
    return render(request, 'accounts/starred_users.html', context)
# -----------------------------------------------------------------

@login_required(login_url='login')
def user_profile(request, pk):
    user = UserProfile.objects.get(id=pk)
    reviews = Review.objects.filter(user_reviewed=user)
    reviews_avg = reviews.aggregate(Avg('rate'))['rate__avg']
    reviews_count = reviews.count()
    skills = user.skill.all()
    context = {'user': user, 'reviews_avg':reviews_avg, 'reviews_count':reviews_count, 'skills':skills}
    return render(request, 'accounts/user_profile.html', context)
# -----------------------------------------------------------------

@login_required(login_url='login')
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
# -----------------------------------------------------------------

@login_required(login_url='login')
def RemoveStaredUser(request, pk):
    desired_user = UserProfile.objects.get(id=pk)
    user = request.user.userprofile
    if request.method == 'POST':
        user.desired_user.remove(desired_user)
        return redirect('starred_users')
   
    context = {'desired_user': desired_user}
    return render(request, 'accounts/RemoveDesiredUser.html', context)

# -----------------------------------------------------------------

@login_required(login_url='login')
def admin_users(request):
    user_p = get_user_model()
    users = user_p.objects.all()
    all_users = users.exclude(username=request.user)

    context = {'all_users': all_users}
    return render(request, 'accounts/admin-users.html', context)

# -----------------------------------------------------------------
@login_required(login_url='login')
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

# -----------------------------------------------------------------

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


# -----------------------------------------------------------------

@login_required(login_url='login')
def searched_users(request):
    user_p = get_user_model()
   

    if request.method == 'POST':
        searched = request.POST['search']
        user_searched = user_p.objects.filter(first_name__contains=searched) | user_p.objects.filter(last_name__contains=searched)
         
    context = {'user_searched': user_searched, 'searched':searched }
    return render(request, 'accounts/searched_users.html', context)



# -----------------------------------------------------------------

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "accounts/password/password_reset_email.txt"
                    c = {
                    "email":user.email,
                    'domain':'127.0.0.1:8000',
                    'site_name': 'Website',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'nohaila1999elhadri@gmail.com' , [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    messages.success(request, 'A message with reset password instructions has been sent to your Email.')
                    return redirect ("homepage")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="accounts/password/password_reset.html", context={"password_reset_form":password_reset_form})


# -----------------------------------------------------------------

@login_required(login_url='login')
def Skill(request):
    pform = PersonalSkillForm()
    if request.method == 'POST':
        pform = PersonalSkillForm(request.POST)
        if pform.is_valid():
            pskills = pform.save()
            request.user.userprofile.personalskill.add(pskills.id)
            return redirect('profile')
    
    context = {'pform':pform}
    return render(request, 'accounts/add_skills.html', context)
