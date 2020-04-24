from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Elections
from blog.models import Society

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username' , 'email' , 'password1','password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email' ]

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class RequestMembershipForm(forms.ModelForm):
    username = forms.CharField(max_length = 100,disabled = True)
    email = forms.EmailField(disabled = True)
    id = forms.IntegerField(disabled = True)

    class Meta:
        model = User
        fields = ['username' , 'email', 'id']

class ApproveMembershipForm(forms.ModelForm):
    username = forms.CharField(max_length = 100, disabled = True)
    email = forms.EmailField(disabled = True)
    id = forms.IntegerField(disabled = True)
    class Meta:
        model = User
        fields = ['username', 'email','id']


class ConductElectionsForm(forms.ModelForm):
    class Meta:
        model = Elections 
        fields = ['Name', 'Discription']