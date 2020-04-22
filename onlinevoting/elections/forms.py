from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from blog.models import Society
from .models import Participant

class ApplyForParticipant(forms.ModelForm):
	class Meta:
		model = Participant
		fields = ['Name', 'Manifesto']
