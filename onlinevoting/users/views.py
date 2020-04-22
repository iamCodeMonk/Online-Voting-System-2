from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView,CreateView,DeleteView
from django.contrib import messages
from .decorators import member_login_required
from blog.models import Society
from django.contrib.auth.models import User
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,RequestMembershipForm, ApproveMembershipForm

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


# class SocietyDetailView(PermissionRequiredMixin,DetailView):
#     model = Society
#     permission_required = ('society.can_view', 'society.can_edit')
#     template_name = 'users/society_detail.html'

@login_required
def SocietyAdminView(request,id):
    if bool(request.user.society_set.filter(id = id).first()):
        return render(request, 'users/society_admin.html', {'society':Society.objects.get(pk = id)})
    else:
        return redirect('My Societies')

@login_required
def SocietyDetailView(request,id):
    if bool(request.user.society_set.filter(id = id).first()):
        return SocietyAdminView(request,id)
    elif bool(request.user.member.socities.filter(id = id)):
        return render(request, 'users/society_detail.html',{'society':Society.objects.get(pk = id)})
    else:
        if request.method == 'POST':
            form = RequestMembershipForm(request.POST, instance = request.user)
            if form.is_valid():
                Society.objects.get(pk = id).Pending_List.add(request.user)
                messages.success(request, f'Your Request Has been Listed')
                return redirect('My Societies')
        else:
            form = RequestMembershipForm(instance = request.user)
            return render(request, 'users/member_request.html',{'form':form})

@login_required
def SocietyApprovalView(request,id1,id2):
    if bool(request.user.society_set.get(id = id1)):
        user = User.objects.get(id = id2)
        society = Society.objects.get(pk = id1)
        if request.method == 'POST':
            form = ApproveMembershipForm(request.POST, instance = user)
            if form.is_valid():
                user = User.objects.get(id = id2)
                user.member.socities.add(Society.objects.get(pk = id1))
                society.Pending_List.remove(user)
                return redirect('My Societies')
        form = ApproveMembershipForm(instance = user)
        return render(request, 'users/society_approve.html', {'form':form})
    else:
        return redirect('My Societies')

class SocietyCreateView(LoginRequiredMixin, CreateView):
    model = Society
    template_name = 'users/society_form.html'
    fields = ['Name','Discription']

    def form_valid(self,form):
        form.instance.Admin = self.request.user
        super().form_valid(form)


class SocietyDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Society

    def test_func(self):
        post = self.get_object()
        if self.request.user == society.Admin:
            return True
        return False
# Create your views here.
