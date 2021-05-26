from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
from .models import *



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']



class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user', 'desired_user']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']







class RateForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    rate = forms.ChoiceField(choices=RATE_CHOICES, widget=forms.Select(), required=True)
    class Meta:
        model = Review
        fields = ('text', 'rate')
