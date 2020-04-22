from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView,CreateView
from django.contrib import messages
from blog.models import Society
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm




def is_member(self,id):
    if bool(self.user.member.socities.get(pk = id)):
        return True
    else:
        return False
mem_login_required = user_passes_test(lambda u: True if is_member(self,id) else False, login_url='login')

def member_login_required(view_func):
    decorated_view_func = login_required(mem_login_required(view_func), login_url='login')
    return decorated_view_func
