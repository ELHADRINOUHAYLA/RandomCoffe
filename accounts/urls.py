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
    path('random/', views.userrandom, name='random'),




]