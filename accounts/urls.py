from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
     
    path('', views.homepage, name="homepage"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    path('about.html/', views.about, name="about"),

    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('users_profile/', views.users_profile, name='users_profile'),
    path('starred_users/', views.starred_users, name='starred_users'),
    path('user_profile/<str:pk>/', views.user_profile, name='user_profile'),
    path('rate_user/<str:pk>/', views.Rate, name='rate_user'),


    path('remove_stared_user/<str:pk>/', views.RemoveStaredUser, name='remove_stared_user'),
    path('admin_users/', views.admin_users, name="admin_users"),
    path('delete_user/<str:pk>/', views.delete_user, name="delete_user"),

    
    path('admin_edit_profile/<str:pk>/', views.admin_edit_profile, name='admin_edit_profile'),
    path('admin_edit_profile/', views.change_password, name='change_password'),
    path('searched_users/', views.searched_users, name='searched-users'),

    path('password_reset/', views.password_reset_request, name="password_reset"),
    path('add_skills/', views.Skill, name="add_skills"),
    path('free_date/', views.Freedate, name="free_date"),
    path('ajax/validate_username/', views.validate_username, name='validate_username'),
    path('search-users', csrf_exempt(views.search_users), name="search_users"),
    path('admin_meetings/', views.admin_meeting, name="meeting"),
    path('settings/', views.settings, name="settings"),
    path('delete-account/', views.delete_acc, name="delete_account"),
    path('meeting_state/', views.MeetingState, name="meeting_state"),
    path('email_sender/', views.Meeting_mail, name="email_sender"),
    path('review_meeting/', views.ReviewMeeting, name="ReviewMeeting"), 



]