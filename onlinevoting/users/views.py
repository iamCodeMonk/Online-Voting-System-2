from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import DetailView,CreateView
from django.contrib import messages
from blog.models import Society
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created for {username}! Now you can login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance = request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your Account Has been Updated')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance = request.user)
        p_form = ProfileUpdateForm(instance = request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def society(request):
    return render(request, 'users/society.html')

class SocietyDetailView(DetailView):
    model = Society
    template_name = 'users/society_detail.html'

class SocietyCreateView(CreateView):
    model = Society
    template_name = 'users/society_form.html'
    fields = ['Name','Discription']

    def form_valid(self,form):
        form.instance.Admin = self.request.user
        super().form_valid(form)

# Create your views here.
