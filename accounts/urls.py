from django.urls import path
from . import views


urlpatterns = [
     
    path('', views.homepage, name="homepage"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
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
    path('about.html/', views.about, name="about"),
    path('random/', views.userrandom, name='random'),




]