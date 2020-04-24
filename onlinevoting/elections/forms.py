from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from blog.models import Society
from .models import Participant

class ApplyForParticipant(forms.ModelForm):
	class Meta:
		model = Participant
		fields = ['Name', 'Manifesto']


class VoteCandidate(forms.ModelForm):
    Name = forms.CharField(max_length = 100,disabled = True)
    Manifesto = forms.CharField(disabled = True)
    class Meta:
        model = Participant
        fields = ['Name', 'Manifesto']

