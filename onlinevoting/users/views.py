from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView,CreateView,DeleteView,ListView
from django.contrib import messages
from .decorators import member_login_required
from blog.models import Society
from django.contrib.auth.models import User
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,RequestMembershipForm, ApproveMembershipForm, ConductElectionsForm
from django.urls import reverse_lazy
from elections.forms import ApplyForParticipant,VoteCandidate
from elections.models import Participant
from .models import Profile

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

# @login_required
# def society(request):
#     return render(request, 'users/society.html')
@login_required
def society(request):
    search_name = ''
    societies= request.user.society_set.all()
    total_societies= Society.objects.all()
    res=[]
    if 'search' in request.GET:
        search_name = request.GET['search']
        for society in total_societies:
            if search_name in society.Name:
                res.insert(0,society)
            societies=res
        context = {
            'societies' : societies,
            'search_name' : search_name
        }
        return render(request, 'users/search_society.html',context)
    context = {
        'societies' : societies,
        'search_name' : search_name
    }
    return render(request, 'users/society.html',context)

# @login_required
# def searchsociety(request):
#     search_name = ''
#     total_societies= Society.objects.all()
#     societies=[]
#     if 'search' in request.GET:
#         search_name = request.GET['search']
#         for society in total_societies:
#             if search_name in society.Name:
#                 societies.insert(0,society)
#     context = {
#         'societies': societies,
#     }
#     return render(request, 'users/search_society.html',context)

@login_required
def ResultsView(request, id):
    if bool(request.user.member.socities.filter(id = id)) or bool(request.user.society_set.filter(id = id)):
        return render(request, 'users/society_results.html',{'society':Society.objects.get(id = id)})

    messages.error(request, f'You Need to be a member View the results')
    return redirect('My Societies')

def ConductElections(request, id):
    if bool(request.user.society_set.filter(id = id).first()):
        society = Society.objects.filter(id = id).first()

        if not society.Voting_process_on:
            if request.method == 'POST':
                form = ConductElectionsForm(request.POST)    
                if form.is_valid():
                    form.instance.society = society
                    society.Voting_process_on = True
                    society.Participation_on = True
                    form.save()
                    society.save()
                    messages.success(request, f'The Election has now been Listed')
                    return redirect('society-detail', id)
            form = ConductElectionsForm()
            return render(request, 'users/society_conduct_vote.html',{'form':form})

        elif society.Voting_process_on and society.Participation_on:
            if request.method == 'POST':
                form = ConductElectionsForm(request.POST, instance = society.elections_set.last())
                if form.is_valid():
                    society.Voting_on = True
                    society.Participation_on = False
                    society.save()
                    messages.success(request, f'The Voting Phase has now begun')
                    return redirect('society-detail', id)

            form = ConductElectionsForm(instance = society.elections_set.last())
            return render(request, 'users/society_conduct_vote.html',{'form':form}) 

        else:
            if request.method == 'POST':
                form = ConductElectionsForm(request.POST, instance = society.elections_set.last())
                if form.is_valid():
                    society.Voting_process_on = False
                    society.Voting_on = False
                    society.save()
                    messages.success(request, f'Elections End Now')
                    return redirect('society-detail', id)

            form = ConductElectionsForm(instance = society.elections_set.last())
            return render(request, 'users/society_conduct_vote.html',{'form':form})

    else:
        return redirect('My Societies')


@login_required
def SocietyAdminView(request,id):
    if bool(request.user.society_set.filter(id = id).first()):
        return render(request, 'users/society_admin.html', {'society':Society.objects.filter(id = id).first()})
    else:
        return redirect('My Societies')

@login_required
def SocietyDetailView(request,id):
    if bool(request.user.society_set.filter(id = id)):
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
                return redirect('society-detail', id1)
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
        form.instance.Participation_on = False
        form.instance.Voting_process_on = False
        form.instance.Voting_on = False
        super().form_valid(form)
        return super().form_valid(form)
    success_url = reverse_lazy('My Societies')


class SocietyDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Society

    def test_func(self):
        society = self.get_object()
        if self.request.user == society.Admin:
            return True
        return False
    success_url = reverse_lazy('My Societies')
# Create your views here.


def ParticipantCreateView(request,id):
    if bool(request.user.member.socities.filter(id = id)) or bool(request.user.society_set.filter(id = id)):
        if Society.objects.filter(id = id).first().Participation_on:
            if request.method == 'POST':
                form = ApplyForParticipant(request.POST)
                form.instance.user = request.user
                society = Society.objects.filter(id = id).first()
                form.instance.elections = society.elections_set.last()
                form.instance.votes = 0
                if form.is_valid() and not bool(society.elections_set.last().participant_set.filter(user_id = request.user.id)):
                    form.save()
                    messages.success(request, f'Your Request Has been Listed')
                    return redirect('society-detail', id)
            form = ApplyForParticipant()
            return render(request, 'users/society_part.html', {'form':form})

        messages.info(request, f'Participation Phase is not active Now')        
        return redirect('society-detail', id)

    messages.error(request, f'You Need to be a member to contest in the elections')
    return redirect('society-detail', id)
# searches for <app>/<model>_form.html
    
def Vote(request,id):
    if bool(request.user.member.socities.filter(id = id)) or bool(request.user.society_set.filter(id = id)):
        if Society.objects.filter(id = id).first().Voting_on:
            return render(request,'users/society_vote.html' ,{'society': Society.objects.filter(id = id).first()})

        messages.info(request, f'Voting Phase is not active Now')        
        return redirect('society-detail', id)

    messages.error(request, f'You Need to be a member to vote in the elections')
    return redirect('My Societies')

def ConfirmVote(request,id1,id2):
    if bool(request.user.member.socities.filter(id = id1)) or bool(request.user.society_set.filter(id = id1)):
        society = Society.objects.filter(id = id1).first()
        if not bool(society.elections_set.last().whoallvoted.filter(id = id2)):
            use = User.objects.filter(id = id2).first()
            participant = society.elections_set.last().participant_set.filter(user_id = id2).first()
            form = VoteCandidate(instance = participant)
            if request.method == 'POST':
                user = request.user
                participant.votes += 1
                participant.save()
                society.elections_set.last().whoallvoted.add(user)
                messages.success(request, f'Thank You for Voting!')
                return redirect('society-detail', id1)
            return render(request,'users/society_confirm_vote.html' ,{'form': form})

        messages.error(request, f'You Cannot Vote More Than Once')
        return redirect('society-detail', id1)

    messages.error(request, f'You Need to be a member to vote in the elections')
    return redirect('My Societies')

