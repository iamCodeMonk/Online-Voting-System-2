from django.db import models
from django.contrib.auth.models import User
from blog.models import Society
from users.models import Elections

class Participant(models.Model):
	Name = models.CharField(max_length = 100)
	Manifesto = models.TextField()
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	elections = models.ForeignKey(Elections, on_delete = models.CASCADE)
	votes = models.IntegerField()
	
	def __str__(self):
		return self.Name




# Create your models here.
