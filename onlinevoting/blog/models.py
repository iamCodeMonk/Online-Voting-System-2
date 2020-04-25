from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Society(models.Model):
    Name = models.CharField(max_length = 100)
    Discription = models.TextField()
    Admin = models.ForeignKey(User, on_delete = models.CASCADE)
    Pending_List = models.ManyToManyField(User, related_name = 'pending_list')
    Participation_on = models.BooleanField()
    Voting_on = models.BooleanField()
    Voting_process_on = models.BooleanField()
    
    def __str__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('society-detail', kwargs={'id': self.society.pk})

# Create your models here.
