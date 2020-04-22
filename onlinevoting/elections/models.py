from django.db import models
from django.contrib.auth.models import User
from blog.models import Society

class Participant(models.Model):
	Name = models.CharField(max_length = 100)
	Manifesto = models.TextField()
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	society = models.ForeignKey(Society, on_delete = models.CASCADE)
	votes = models.IntegerField(default = 0)
	
	def __str__(self):
		return self.Name

# Create your models here.
